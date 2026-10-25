#!/usr/bin/env python3
"""Montage automatique d'une séquence de gameplay en vidéo verticale Shorts/TikTok.

Utilise FFmpeg pour :
  - recadrer en 1080x1920 (9:16),
  - ajouter l'accroche (hook) en haut de l'écran,
  - ajouter le CTA en bas,
  - ajouter une outro « STARCRUISER CLICKER — Play for free ».

Exemple :
    python scripts/build_video.py \
        --input assets/sequences/run.mp4 \
        --hook "One click. One galaxy. How far can you go? 🚀" \
        --cta "Play for free: starcruiserclicker.com" \
        --output out/short.mp4
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GAME_NAME = "STARCRUISER CLICKER"
OUTRO_TEXT = "Play for free >> starcruiserclicker.com"


def esc(text: str) -> str:
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace("%", "\\%")


def has_audio(path: str) -> bool:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
             "stream=codec_type", "-of", "csv=p=0", path],
            capture_output=True, text=True, check=True,
        )
        return "audio" in out.stdout
    except subprocess.CalledProcessError:
        return False


def build(input_path: Path, hook: str, cta: str, output: Path,
          duration: float | None, outro_seconds: float, font: str | None) -> None:
    if shutil.which("ffmpeg") is None:
        sys.exit("Erreur : FFmpeg est requis. Installe-le avec 'apt install ffmpeg' ou via brew.")
    if not input_path.exists():
        sys.exit(f"Erreur : séquence introuvable : {input_path}")

    output.parent.mkdir(parents=True, exist_ok=True)
    font_opt = f":fontfile={font}" if font else ""

    filters = (
        # recadrage vertical 9:16 centré, puis format final
        f"crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',"
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        # accroche en haut
        f"drawtext=text='{esc(hook)}':fontcolor=white:fontsize=54:x=(w-text_w)/2:y=180:"
        f"box=1:boxcolor=black@0.55:boxborderw=18{font_opt},"
        # CTA en bas
        f"drawtext=text='{esc(cta)}':fontcolor=white:fontsize=42:x=(w-text_w)/2:y=1500:"
        f"box=1:boxcolor=black@0.55:boxborderw=14{font_opt}"
    )

    with tempfile.TemporaryDirectory() as tmp:
        body = Path(tmp) / "body.mp4"
        cmd = ["ffmpeg", "-y", "-i", str(input_path)]
        if duration:
            cmd += ["-t", str(duration)]
        if has_audio(str(input_path)):
            cmd += ["-c:a", "aac", "-b:a", "128k"]
        else:
            cmd += ["-an"]
        cmd += ["-vf", filters, "-c:v", "libx264", "-preset", "fast",
                "-pix_fmt", "yuv420p", "-r", "30", str(body)]
        subprocess.run(cmd, check=True)

        # outro : fond noir + nom du jeu + lien
        outro = Path(tmp) / "outro.mp4"
        outro_filters = (
            f"color=c=black:s=1080x1920:d={outro_seconds}:r=30[bg];"
            f"[bg]drawtext=text='{esc(GAME_NAME)}':fontcolor=white:fontsize=72:"
            f"x=(w-text_w)/2:y=850{font_opt},"
            f"drawtext=text='{esc(OUTRO_TEXT)}':fontcolor=white:fontsize=44:"
            f"x=(w-text_w)/2:y=980{font_opt}[v]"
        )
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i",
             f"color=c=black:s=1080x1920:d={outro_seconds}:r=30",
             "-filter_complex", outro_filters, "-map", "[v]",
             "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(outro)],
            check=True,
        )

        subprocess.run(
            ["ffmpeg", "-y", "-i", str(body), "-i", str(outro),
             "-filter_complex", "[0:v][0:a][1:v]concat=n=2:v=1:a=1[outv][outa]",
             "-map", "[outv]", "-map", "[outa]",
             "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(output)],
            check=True,
        )
        print(f"✅ Vidéo générée : {output} ({output.stat().st_size // 1024} Ko)")


def main() -> None:
    p = argparse.ArgumentParser(description="Montage Shorts/TikTok pour Starcruiser Clicker")
    p.add_argument("--input", required=True, help="Séquence de gameplay source")
    p.add_argument("--hook", required=True, help="Accroche affichée en haut")
    p.add_argument("--cta", required=True, help="Appel à l'action affiché en bas")
    p.add_argument("--output", required=True, help="Fichier de sortie (.mp4)")
    p.add_argument("--duration", type=float, default=None, help="Durée du corps en secondes")
    p.add_argument("--outro-seconds", type=float, default=2.5, help="Durée de l'outro")
    p.add_argument("--font", default=None, help="Chemin d'une police TTF optionnelle")
    a = p.parse_args()
    build(Path(a.input), a.hook, a.cta, Path(a.output), a.duration, a.outro_seconds, a.font)


if __name__ == "__main__":
    main()
