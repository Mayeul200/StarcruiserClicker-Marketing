#!/usr/bin/env python3
"""Renderer v2 : pack « pro simple » — transitions, Ken Burns, textes animés.

Effets :
  - Ken Burns : zoom lent continu (1.00 -> 1.06) sur chaque séquence
  - crossfade 0.2s entre les séquences (xfade)
  - apparition animée du mot-clé : fade-in + zoom-in pendant 0.25s
  - vignettage léger sur l'image (bords assombris)
  - barre de progression des étapes en haut (points qui se remplissent)
  - flash blanc court (2 frames) en début de chaque séquence pour l'énergie

Usage :
    python scripts/make_video.py video-plans/v1-concept.json
"""

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception as e:
    print(f"Erreur : pip install imageio-ffmpeg\n{e}")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SEQ = ROOT / "assets" / "sequences"
OUT = ROOT / "out"
LOGO = SEQ / "logo2.png"

W, H = 1080, 1920
BG_BLUE = (10, 14, 26)
CTA_Y = 1615
FG_H = 1166  # hauteur de la bande de jeu
LOGO_Y = 1700
KEYWORD_Y = 150
SUB_Y = 330
XFADE_D = 0.2   # durée du crossfade
KB_ZOOM = 1.06  # zoom final Ken Burns
TXT_ANIM_D = 0.25  # apparition du mot-clé (s)
FPS = 30


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        sys.exit(1)


def probe_duration(path: Path) -> float:
    r = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "Duration:" in line:
            t = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = t.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


def load_font(size: int):
    import matplotlib
    mp = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    for cand in (mp / "DejaVuSans-Bold.ttf", mp / "DejaVuSans.ttf"):
        if cand.exists():
            return ImageFont.truetype(str(cand), size)
    return ImageFont.load_default()


def text_with_shadow(d, xy, text, font, fill, shadow=(0, 0, 0, 220), offset=6):
    x, y = xy
    d.text((x + offset, y + offset), text, font=font, fill=shadow)
    d.text((x, y), text, font=font, fill=fill)


def cta_png(path: Path, text: str) -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = load_font(44)
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    pad_x, pad_y = 34, 20
    x1, y1 = (W - tw) // 2 - pad_x, CTA_Y - pad_y
    x2, y2 = (W + tw) // 2 + pad_x, CTA_Y + bbox[3] + pad_y
    d.rounded_rectangle([x1, y1, x2, y2], radius=y2 - y1, fill=(0, 0, 0, 170))
    d.rounded_rectangle([x1, y1, x2, y2], radius=y2 - y1, outline=(126, 200, 255, 200), width=3)
    d.text(((W - tw) // 2, CTA_Y - bbox[1]), text, font=font, fill="white")
    img.save(path)
    return path


def big_png(path: Path, big: str, sub: str | None) -> Path:
    """Mot-clé doré + sous-titre, pour apparition animée (fade+zoom)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # taille auto : le texte ne doit jamais dépasser ~92% de la largeur
    size = 132
    while size > 40:
        f = load_font(size)
        bb = d.textbbox((0, 0), big, font=f)
        if bb[2] - bb[0] <= int(W * 0.92):
            break
        size -= 8
    font = load_font(size)
    bbox = d.textbbox((0, 0), big, font=font)
    tw = bbox[2] - bbox[0]
    cx, y = W // 2, KEYWORD_Y
    for off, col in ((10, (0, 0, 0, 200)), (5, (0, 0, 0, 255))):
        d.text((cx - tw // 2 + off, y - bbox[1] + off), big, font=font, fill=col)
    d.text((cx - tw // 2 - 3, y - bbox[1] - 3), big, font=font, fill=(255, 215, 100))
    d.text((cx - tw // 2, y - bbox[1]), big, font=font, fill=(255, 230, 140))
    if sub:
        f2 = load_font(50)
        b2 = d.textbbox((0, 0), sub, font=f2)
        sw = b2[2] - b2[0]
        text_with_shadow(d, (cx - sw // 2, SUB_Y - b2[1]), sub, f2, "white")
    img.save(path)
    return path


def steps_png(path: Path, total: int, current: int) -> Path:
    """Vraie barre de progression : track fin + remplissage continu doré.

    Chaque séquence génère une frame de remplissage proportionnelle —
    les frames successives des clips donnent une progression fluide.
    """
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bar_w = 760
    bar_h = 10
    x1 = (W - bar_w) // 2
    y = 76
    # track de fond (arrondi, translucide)
    d.rounded_rectangle([x1, y, x1 + bar_w, y + bar_h], radius=bar_h // 2,
                        fill=(255, 255, 255, 60))
    # remplissage doré jusqu'à l'étape courante (dégradé ambré)
    fill_w = int(bar_w * current / total)
    if fill_w > 0:
        for k in range(fill_w):
            t = k / max(fill_w - 1, 1)
            col = (int(255 - 30 * t), int(215 - 15 * t), int(100 + 40 * t), 255)
            d.line([x1 + k, y + 1, x1 + k, y + bar_h - 1], fill=col)
    # petit point lumineux au bout du remplissage
    if fill_w > 4:
        d.ellipse([x1 + fill_w - 5, y - 1, x1 + fill_w + 5, y + bar_h + 1],
                  fill=(255, 240, 180, 255))
    img.save(path)
    return path


def logo_png(path: Path) -> Path:
    img = Image.open(LOGO).convert("RGBA")
    width = 580
    img = img.resize((width, int(img.height * width / img.width)), Image.LANCZOS)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.paste(img, ((W - width) // 2, LOGO_Y), img)
    canvas.save(path)
    return path


def outro_png(path: Path) -> Path:
    base = Image.new("RGBA", (W, H), BG_BLUE + (255,))
    lg = Image.open(LOGO).convert("RGBA")
    lw = 760
    lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    base.paste(lg, ((W - lw) // 2, 720), lg)
    d = ImageDraw.Draw(base)
    fq = load_font(64)
    q = "How far will YOU go?"
    bq = d.textbbox((0, 0), q, font=fq)
    d.text(((W - bq[2]) // 2 + 5, 555 + 5), q, font=fq, fill=(0, 0, 0))
    d.text(((W - bq[2]) // 2, 555), q, font=fq, fill=(255, 215, 100))
    f2 = load_font(42)
    text = "Play free >> starcruiserclicker.com"
    b = d.textbbox((0, 0), text, font=f2)
    d.text(((W - b[2]) // 2, 1010), text, font=f2, fill=(126, 200, 255))
    base.convert("RGB").save(path)
    return path


def vignette_chain() -> str:
    """Vignettage léger : bords assombris (mode cinéma)."""
    return (
        "vignette=PI/5"
    )


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage : python scripts/make_video.py <plan.json>")
        sys.exit(1)
    plan_path = Path(sys.argv[1])
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    OUT.mkdir(exist_ok=True)
    tmp = OUT / "_tmp"
    tmp.mkdir(exist_ok=True)

    cta = cta_png(tmp / "cta.png", plan.get("cta", "Play free: starcruiserclicker.com"))
    logo = logo_png(tmp / "logo.png")

    clips = [c for c in plan["clips"] if (SEQ / c["file"]).exists()]
    n = len(clips)
    # PNG transparent 1x1 pour les clips sans texte (input toujours présent)
    blank = tmp / "blank.png"
    Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(blank)
    # hook plein écran (optionnel, plan["hook"]) : gros texte au tout début
    hook_png_file = None
    if plan.get("hook"):
        hook_png_file = big_png(tmp / "hook.png", plan["hook"], plan.get("hook_sub"))
    parts = []
    for i, clip in enumerate(clips):
        src = SEQ / clip["file"]
        speed = float(clip.get("speed", 1.0))
        dur = probe_duration(src) / speed
        if clip.get("max"):
            dur = min(dur, float(clip["max"]))
        has_text = bool(clip.get("big"))
        big = big_png(tmp / f"big{i}.png", clip["big"], clip.get("sub")) if has_text else blank
        steps = steps_png(tmp / f"steps{i}.png", n, clip.get("progress", i + 1))
        part = tmp / f"part{i}.mp4"
        # hook plein écran sur la 1re séquence (remplace son mot-clé)
        hook_dur = 0.0
        if i == 0 and hook_png_file:
            big = hook_png_file
            hook_dur = float(plan.get("hook_dur", 1.2))
            has_text = True  # le hook EST le texte de la séquence

        if clip.get("crop"):
            x1, y1, x2, y2 = clip["crop"]
            cw, ch = x2 - x1, y2 - y1
            fg_chain = (
                f"crop={cw}:{ch}:{x1}:{y1},"
                f"scale={W}:{FG_H}:force_original_aspect_ratio=increase:flags=area,"
                f"crop={W}:{FG_H},setsar=1"
            )
            bg_chain = (
                f"crop={cw}:{ch}:{x1}:{y1},"
                f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=area,"
                f"crop={W}:{H},gblur=sigma=28,eq=brightness=-0.15,setsar=1"
            )
        else:
            fg_chain = (
                f"scale={W}:-2:flags=area,"
                f"pad={W}:{FG_H}:(ow-iw)/2:(oh-ih)/2:color=0x0a0e1a,setsar=1"
            )
            bg_chain = (
                f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=area,"
                f"crop={W}:{H},gblur=sigma=28,eq=brightness=-0.15,setsar=1"
            )

        # Ken Burns : zoom lent 1.00 -> KB_ZOOM sur la bande composée
        # (appliqué après composition pour zoomer logo + jeu ensemble)
        kb = (
            f"scale={W * 2}:{H * 2},"
            f"zoompan=z='min(zoom+0.00015,{KB_ZOOM})':x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},setsar=1"
        )
        # apparition du mot-clé : fondu d'entrée (simple et fiable)
        if hook_dur > 0:
            big_anim = (
                f"[1:v]format=rgba,fade=t=in:st=0:d=0.15:alpha=1,"
                f"fade=t=out:st={hook_dur - 0.15:.2f}:d=0.15:alpha=1[txt]"
            )
        else:
            big_anim = (
                f"[1:v]format=rgba,fade=t=in:st=0:d={TXT_ANIM_D}:alpha=1[txt]"
            )
        # punch zoom en début de séquence puis Ken Burns continu
        zoom_expr = f"if(lt(on,8),1.08-0.01*on,min(1+0.00015*on,{KB_ZOOM}))"
        punch = (
            f"scale={W * 2}:{H * 2}:flags=area,"
            f"zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d=1:s={W}x{H}:fps={FPS},setsar=1"
        )
        if has_text:
            txt_overlay = f"[b0][txt]overlay=0:0[b1];[b1][2:v]overlay=0:0[b2];"
            last = "[b2]"
        else:
            txt_overlay = ""
            last = "[b0]"
        fc = (
            f"[0:v]setpts={1 / speed:.6f}*PTS,split=2[s1][s2];"
            f"[s1]{bg_chain}[bg];"
            f"[s2]{fg_chain}[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,{vignette_chain()}[b0];"
            + (f"{big_anim};" if has_text else "")
            + txt_overlay
            + f"{last}[3:v]overlay=0:0[bx];"
            f"[bx][4:v]overlay=0:0,"
            f"{punch},"
            f"fade=t=in:st=0:d=0.08:color=white,"
            f"format=yuv420p[vout]"
        )
        run([FF, "-y", "-i", str(src),
             "-loop", "1", "-t", f"{dur:.3f}", "-i", str(big),
             "-loop", "1", "-t", f"{dur:.3f}", "-i", str(steps),
             "-loop", "1", "-t", f"{dur:.3f}", "-i", str(cta),
             "-loop", "1", "-t", f"{dur:.3f}", "-i", str(logo),
             "-filter_complex", fc, "-map", "[vout]", "-an", "-r", str(FPS),
             "-t", f"{dur:.3f}",
             "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(part)])
        parts.append(part)
        print(f"✅ {clip['file']}")

    # assemblage : cuts secs (les flashs blancs marquent chaque étape)
    concat = tmp / "list.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in parts))
    body = tmp / "body.mp4"
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
         "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(body)])

    inputs2 = ["-i", str(body)]
    fc2 = "[0:v]copy[v]"
    if plan.get("outro", True):
        o = outro_png(tmp / "outro.png")
        outro = tmp / "outro.mp4"
        run([FF, "-y", "-loop", "1", "-t", "1.5", "-i", str(o),
             "-vf", "scale=1080:1920,setsar=1,format=yuv420p", "-r", str(FPS), str(outro)])
        inputs2 += ["-i", str(outro)]
        fc2 = "[0:v][1:v]xfade=transition=fade:duration=0.3:offset=" \
              f"{probe_duration(body) - 0.15:.3f}[v]"

    final = OUT / f"{plan['id']}.mp4"
    run([FF, "-y", *inputs2, "-filter_complex", fc2, "-map", "[v]",
         "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", str(final)])
    print(f"OK {final} ({final.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()
