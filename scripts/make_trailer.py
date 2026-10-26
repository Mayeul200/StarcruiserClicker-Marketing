#!/usr/bin/env python3
"""Monte le trailer v2 : paysage complet + fond flouté (plus de recadrage).

Chaque clip 16:9 est affiché EN ENTIER, pleine largeur (1080px), centré
verticalement ; le haut et le bas sont remplis par le même clip flouté et
assombri. L'accroche et le CTA sont incrustés dans les zones floutées.

Les clips sont utilisés INTEGRALEMENT (début -> fin) : à toi de couper
l'extrait au moment exact de l'action avant de le pousser dans le repo.
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


def text_png(path: Path, lines: list[tuple[str, int]], y_start: int) -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = y_start
    for text, size in lines:
        font = load_font(size)
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        pad = 24
        d.rounded_rectangle(
            [(W - tw) // 2 - pad, y - pad // 2, (W + tw) // 2 + pad, y + bbox[3] + pad],
            radius=18, fill=(0, 0, 0, 150),
        )
        d.text(((W - tw) // 2, y - bbox[1]), text, font=font, fill="white")
        y += bbox[3] + bbox[1] + size // 2
    img.save(path)
    return path


def main() -> None:
    OUT.mkdir(exist_ok=True)
    tmp = OUT / "_tmp"
    tmp.mkdir(exist_ok=True)

    hook_png = text_png(tmp / "hook.png", [(l, 56) for l in HOOK_LINES], y_start=140)
    cta_png = text_png(tmp / "cta.png", [(CTA, 44)], y_start=1560)

    # Chaque clip est utilisé EN ENTIER (pas de coupe) — ajuste au besoin la
    # durée max via le 3e element pour éviter les temps morts.
    plan = [
        ("ClicsOnThePart.mp4", "hook", 3.0),
        ("BuyBuildings.mp4", "cta", 4.0),
        ("PopUpNewBuildings.mp4", "cta", 4.0),
        ("AchatDesUpgrades.mp4", "cta", 2.6),
        ("AchatDesPiècesDeFusée.mp4", "cta", 5.0),
        ("LiftoffAndVoyage.mp4", "cta", 8.0),
        ("ContratComète.mp4", "cta", 5.0),
        ("Boosters.mp4", "cta", 6.0),
        ("AffichageAtelierGalactique.mp4", "cta", 5.0),
        ("AffichageStatistiques.mp4", "cta", 4.0),
        ("AffichageLeaderboard.mp4", "cta", 2.5),
    ]

    parts = []
    for i, (name, overlay, max_dur) in enumerate(plan):
        src = SEQ / name
        if not src.exists():
            print(f"⚠️ {name} introuvable, ignoré")
            continue
        part = tmp / f"part{i}.mp4"
        # fond : clip remplit 1080x1920 (crop) puis flouté + assombri
        # avant : clip entier à pleine largeur, centré verticalement
        fc = (
            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=area,"
            f"crop={W}:{H},gblur=sigma=28,eq=brightness=-0.15,setsar=1[bg];"
            f"[0:v]scale={W}:-2,setsar=1[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[b1]"
        )
        if overlay == "hook":
            fc += ";[b1][1:v]overlay[b2];[b2][2:v]overlay[vout]"
            inputs = ["-i", str(hook_png), "-i", str(cta_png)]
        else:
            fc += ";[b1][1:v]overlay[vout]"
            inputs = ["-i", str(cta_png)]
        run([FF, "-y", "-t", str(max_dur), "-i", str(src), *inputs,
             "-filter_complex", fc, "-map", "[vout]", "-an", "-r", "30",
             "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(part)])
        parts.append(part)
        print(f"✅ {name}")

    concat = tmp / "list.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in parts))
    body = tmp / "body.mp4"
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
         "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(body)])

    outro_png = tmp / "outro.png"
    img = Image.new("RGBA", (W, H), BG_BLUE + (255,))
    d = ImageDraw.Draw(img)
    f1 = load_font(68)
    bbox = d.textbbox((0, 0), GAME, font=f1)
    d.text(((W - bbox[2]) // 2, 830), GAME, font=f1, fill="white")
    f2 = load_font(40)
    bbox2 = d.textbbox((0, 0), OUTRO_URL, font=f2)
    d.text(((W - bbox2[2]) // 2, 960), OUTRO_URL, font=f2, fill=(126, 200, 255))
    img.convert("RGB").save(outro_png)

    outro = tmp / "outro.mp4"
    run([FF, "-y", "-loop", "1", "-t", "2.5", "-i", str(outro_png),
         "-vf", "scale=1080:1920,setsar=1,format=yuv420p", "-r", "30", str(outro)])

    final = OUT / "main-trailer.mp4"
    run([FF, "-y", "-i", str(body), "-i", str(outro),
         "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
         "-map", "[v]", "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", str(final)])
    print(f"OK {final} ({final.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()
