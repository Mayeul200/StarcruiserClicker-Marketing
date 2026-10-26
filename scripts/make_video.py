#!/usr/bin/env python3
"""Renderer générique : un plan JSON -> une vidéo Shorts/TikTok punchy.

Format : clip 16:9 entier pleine largeur, fond flouté, logo en haut,
gros mot-clé + sous-titre au milieu, CTA en bas, accélération par clip.

Usage :
    python scripts/make_video.py video-plans/v1-concept.json

Plan JSON :
{
  "id": "v1-concept",
  "cta": "Play free: starcruiserclicker.com",
  "outro": true,
  "clips": [
    {"file": "ClicsOnThePart.mp4", "speed": 1.5,
     "big": "CLICK", "sub": "pour gagner des Parts"},
    ...
  ]
}
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
CTA_Y = 1580


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1200:])
        sys.exit(1)


def load_font(size: int):
    import matplotlib
    mp = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    for cand in (mp / "DejaVuSans-Bold.ttf", mp / "DejaVuSans.ttf"):
        if cand.exists():
            return ImageFont.truetype(str(cand), size)
    return ImageFont.load_default()


def cta_png(path: Path, text: str) -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = load_font(46)
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    pad = 26
    d.rounded_rectangle(
        [(W - tw) // 2 - pad, CTA_Y - pad // 2, (W + tw) // 2 + pad, CTA_Y + bbox[3] + pad],
        radius=20, fill=(0, 0, 0, 160),
    )
    d.text(((W - tw) // 2, CTA_Y - bbox[1]), text, font=font, fill="white")
    img.save(path)
    return path


def big_png(path: Path, big: str, sub: str | None) -> Path:
    """Gros mot-clé + sous-titre, centrés vers le haut de la zone d'action."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = load_font(150)
    bbox = d.textbbox((0, 0), big, font=font)
    tw = bbox[2] - bbox[0]
    pad = 30
    d.rounded_rectangle(
        [(W - tw) // 2 - pad, 250 - pad, (W + tw) // 2 + pad, 250 + bbox[3] + pad],
        radius=24, fill=(126, 200, 255, 235),
    )
    d.text(((W - tw) // 2, 250 - bbox[1]), big, font=font, fill=(10, 14, 26))
    if sub:
        f2 = load_font(52)
        b2 = d.textbbox((0, 0), sub, font=f2)
        d.rounded_rectangle(
            [(W - b2[2]) // 2 - 20, 470, (W + b2[2]) // 2 + 20, 470 + b2[3] + 44],
            radius=16, fill=(0, 0, 0, 160),
        )
        d.text(((W - b2[2]) // 2, 470 + 20), sub, font=f2, fill="white")
    img.save(path)
    return path


def logo_png(path: Path) -> Path:
    img = Image.open(LOGO).convert("RGBA")
    width = 540
    img = img.resize((width, int(img.height * width / img.width)), Image.LANCZOS)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.paste(img, ((W - width) // 2, 60), img)
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

    parts = []
    for i, clip in enumerate(plan["clips"]):
        src = SEQ / clip["file"]
        if not src.exists():
            print(f"⚠️ {clip['file']} introuvable, ignoré")
            continue
        speed = float(clip.get("speed", 1.0))
        big = big_png(tmp / f"big{i}.png", clip["big"], clip.get("sub"))
        part = tmp / f"part{i}.mp4"
        # crop ciblé : [x1, y1, x2, y2] sur la source -> zoom sur une zone
        # précise ; sinon crop 9:16 plein écran (jeu entier visible)
        if clip.get("crop"):
            x1, y1, x2, y2 = clip["crop"]
            cw, ch = x2 - x1, y2 - y1
            # la zone cropée est affichée à pleine largeur (bande centrale),
            # et le MÊME crop flouté remplit le haut/bas -> bandes floutées
            fg_chain = (
                f"crop={cw}:{ch}:{x1}:{y1},"
                f"scale={W}:-2:flags=area,setsar=1"
            )
            bg_chain = (
                f"crop={cw}:{ch}:{x1}:{y1},"
                f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=area,"
                f"crop={W}:{H},gblur=sigma=28,eq=brightness=-0.15,setsar=1"
            )
        else:
            fg_chain = f"scale={W}:-2,setsar=1"
            bg_chain = (
                f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=area,"
                f"crop={W}:{H},gblur=sigma=28,eq=brightness=-0.15,setsar=1"
            )
        fc = (
            f"[0:v]setpts={1 / speed:.6f}*PTS,split=2[s1][s2];"
            f"[s1]{bg_chain}[bg];"
            f"[s2]{fg_chain}[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[b0];"
            f"[b0][1:v]overlay=0:0,setsar=1[b1];"
            f"[b1][2:v]overlay=0:0,setsar=1[b2];"
            f"[b2][3:v]overlay=0:0[vout]"
        )
        run([FF, "-y", "-i", str(src), "-i", str(logo), "-i", str(big), "-i", str(cta),
             "-filter_complex", fc, "-map", "[vout]", "-an", "-r", "30",
             "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(part)])
        parts.append(part)

    concat = tmp / "list.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in parts))
    body = tmp / "body.mp4"
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
         "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(body)])

    inputs = ["-i", str(body)]
    fc = "[0:v]copy[v]"
    if plan.get("outro", True):
        o = outro_png(tmp / "outro.png")
        outro = tmp / "outro.mp4"
        run([FF, "-y", "-loop", "1", "-t", "1.5", "-i", str(o),
             "-vf", "scale=1080:1920,setsar=1,format=yuv420p", "-r", "30", str(outro)])
        inputs += ["-i", str(outro)]
        fc = "[0:v][1:v]concat=n=2:v=1:a=0[v]"

    final = OUT / f"{plan['id']}.mp4"
    run([FF, "-y", *inputs, "-filter_complex", fc, "-map", "[v]",
         "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", str(final)])
    print(f"OK {final} ({final.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()
