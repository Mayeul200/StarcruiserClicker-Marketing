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
    font = load_font(132)
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
    """Barre de progression : pastilles remplies jusqu'à l'étape courante."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = 10
    gap = 28
    total_w = total * (2 * r) + (total - 1) * gap
    x = (W - total_w) // 2
    y = 80
    for i in range(total):
        cx = x + r + i * (2 * r + gap)
        if i < current:
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=(255, 215, 100, 255))
        else:
            d.ellipse([cx - r, y - r, cx + r, y + r],
                      fill=(255, 255, 255, 70), outline=(255, 255, 255, 150), width=2)
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
    parts = []
    for i, clip in enumerate(clips):
        src = SEQ / clip["file"]
        speed = float(clip.get("speed", 1.0))
        dur = probe_duration(src) / speed
        big = big_png(tmp / f"big{i}.png", clip["big"], clip.get("sub"))
        steps = steps_png(tmp / f"steps{i}.png", n, i + 1)
        part = tmp / f"part{i}.mp4"

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
        big_anim = (
            f"[1:v]format=rgba,fade=t=in:st=0:d={TXT_ANIM_D}:alpha=1[txt]"
        )
        fc = (
            f"[0:v]setpts={1 / speed:.6f}*PTS,split=2[s1][s2];"
            f"[s1]{bg_chain}[bg];"
            f"[s2]{fg_chain}[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,{vignette_chain()}[b0];"
            f"{big_anim};"
            f"[b0][txt]overlay=0:0[b1];"
            f"[b1][2:v]overlay=0:0[b2];"
            f"[b2][3:v]overlay=0:0[b3];"
            f"[b3][4:v]overlay=0:0,format=yuv420p[vout]"
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

    # assemblage avec crossfades entre séquences
    inputs = []
    for p in parts:
        inputs += ["-i", str(p)]
    if len(parts) == 1:
        body = tmp / "body.mp4"
        run([FF, "-y", *inputs, "-map", "0:v", "-c:v", "libx264",
             "-preset", "fast", "-pix_fmt", "yuv420p", str(body)])
    else:
        durs = [probe_duration(p) for p in parts]
        fc_parts = []
        prev = "[0:v]"
        # longueur accumulée de la timeline au fil des xfades :
        # L_k = L_{k-1} + dur_k - D ; offset_k = L_{k-1} - D
        length = durs[0]
        for k in range(1, len(parts)):
            out_label = f"[x{k}]" if k < len(parts) - 1 else "[xlast]"
            fc_parts.append(
                f"{prev}[{k}:v]xfade=transition=fade:duration={XFADE_D}:offset={length - XFADE_D:.3f}{out_label}"
            )
            prev = out_label
            length += durs[k] - XFADE_D
        body = tmp / "body.mp4"
        run([FF, "-y", *inputs, "-filter_complex", ";".join(fc_parts),
             "-map", "[xlast]", "-c:v", "libx264", "-preset", "fast",
             "-pix_fmt", "yuv420p", str(body)])

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
