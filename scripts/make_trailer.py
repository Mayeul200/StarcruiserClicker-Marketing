#!/usr/bin/env python3
"""Monte la 1re vidéo trailer à partir des extraits existants.

Recadre chaque extrait en 1080x1920 (crop central), incruste l'accroche et
le CTA via des PNG générés par PIL (le ffmpeg embarqué n'a pas drawtext),
concatène, ajoute l'outro, et produit out/main-trailer.mp4.
"""

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception as e:
    print(f"Erreur : imageio-ffmpeg introuvable. Lance : pip install imageio-ffmpeg\n{e}")
    sys.exit(1)
ROOT = Path(__file__).resolve().parent.parent
SEQ = ROOT / "assets" / "sequences"
OUT = ROOT / "out"

W, H = 1080, 1920
HOOK_LINES = ["One click. One galaxy.", "How far can you go? 🚀"]
CTA = "Play for free: starcruiserclicker.com"
GAME = "STARCRUISER CLICKER"
OUTRO_URL = "Play for free >> starcruiserclicker.com"
BG_BLUE = (10, 14, 26)


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1200:])
        sys.exit(1)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    import matplotlib
    mp = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    for cand in (
        mp / "DejaVuSans-Bold.ttf",
        mp / "DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if cand.exists():
            return ImageFont.truetype(str(cand), size)
    return ImageFont.load_default()


def text_png(path: Path, lines: list[tuple[str, int, int]], y_start: int) -> Path:
    """Génère un PNG transparent avec des blocs de texte (texte, taille, y)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = y_start
    for text, size, _ in lines:
        font = load_font(size)
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        pad = 24
        d.rounded_rectangle(
            [(W - tw) // 2 - pad, y - pad // 2, (W + tw) // 2 + pad, y + bbox[3] + pad],
            radius=18, fill=(0, 0, 0, 145),
        )
        d.text(((W - tw) // 2, y - bbox[1]), text, font=font, fill="white")
        y += bbox[3] + bbox[1] + size // 2
    img.save(path)
    return path


def main() -> None:
    OUT.mkdir(exist_ok=True)
    tmp = OUT / "_tmp"
    tmp.mkdir(exist_ok=True)

    hook_png = tmp / "hook.png"
    text_png(hook_png, [(HOOK_LINES[0], 56, 0), (HOOK_LINES[1], 56, 0)], y_start=150)
    cta_png = tmp / "cta.png"
    text_png(cta_png, [(CTA, 40, 0)], y_start=1500)

    plan = [
        ("ClicsOnThePart.mp4", 0.0, 2.4, "hook"),
        ("BuyBuildings.mp4", 0.0, 4.0, "cta"),
        ("PopUpNewBuildings.mp4", 0.0, 3.5, "cta"),
        ("Boosters.mp4", 0.0, 4.5, "cta"),
        ("AffichageAtelierGalactique.mp4", 0.5, 4.5, "cta"),
    ]

    parts = []
    for i, (name, start, dur, overlay) in enumerate(plan):
        src = SEQ / name
        part = tmp / f"part{i}.mp4"
        vf = (
            f"crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',"
            f"scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,setsar=1,format=yuv420p"
        )
        if overlay == "hook":
            fc = (f"[0:v]{vf}[b];[b][1:v]overlay=0:0[t];[t][2:v]overlay=0:0[vout]")
            run([FF, "-y", "-ss", str(start), "-t", str(dur), "-i", str(src),
                 "-i", str(hook_png), "-i", str(cta_png),
                 "-filter_complex", fc,
                 "-map", "[vout]", "-an", "-r", "30", str(part)])
        else:
            fc = f"[0:v]{vf}[b];[b][1:v]overlay=0:0[vout]"
            run([FF, "-y", "-ss", str(start), "-t", str(dur), "-i", str(src),
                 "-i", str(cta_png),
                 "-filter_complex", fc,
                 "-map", "[vout]", "-an", "-r", "30", str(part)])
        parts.append(part)

    concat = tmp / "list.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in parts))
    body = tmp / "body.mp4"
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
         "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(body)])

    outro_png = tmp / "outro.png"
    img = Image.new("RGBA", (W, H), BG_BLUE + (255,))
    d = ImageDraw.Draw(img)
    f1 = load_font(68)
    t = GAME
    bbox = d.textbbox((0, 0), t, font=f1)
    d.text(((W - bbox[2]) // 2, 830), t, font=f1, fill="white")
    f2 = load_font(40)
    t2 = OUTRO_URL
    bbox2 = d.textbbox((0, 0), t2, font=f2)
    d.text(((W - bbox2[2]) // 2, 960), t2, font=f2, fill=(126, 200, 255))
    img.convert("RGB").save(outro_png)

    outro = tmp / "outro.mp4"
    run([FF, "-y", "-loop", "1", "-t", "2.5", "-i", str(outro_png),
         "-vf", "format=yuv420p", "-r", "30", str(outro)])

    final = OUT / "main-trailer.mp4"
    run([FF, "-y", "-i", str(body), "-i", str(outro),
         "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
         "-map", "[v]", "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", str(final)])
    print(f"OK {final} ({final.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()
