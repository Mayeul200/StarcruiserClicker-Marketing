#!/usr/bin/env python3
"""Génère TOUTES les vidéos : plans principaux + variantes.

Usage :
    python scripts/make_all.py              # tout
    python scripts/make_all.py v1            # tous les plans v1*
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
plans = sorted(
    list((ROOT / "video-plans").glob("v*.json"))
    + list((ROOT / "video-plans" / "variants").glob("v*.json"))
)
if len(sys.argv) > 1:
    prefix = sys.argv[1]
    plans = [p for p in plans if p.stem.startswith(prefix)]

print(f"{len(plans)} plan(s) à générer")
failed = []
for p in plans:
    print(f"\n=== {p.stem} ===")
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "make_video.py"), str(p)])
    if r.returncode != 0:
        failed.append(p.stem)

print("\n" + "=" * 40)
if failed:
    print(f"❌ Échecs : {', '.join(failed)}")
    sys.exit(1)
print(f"✅ {len(plans)} vidéos générées dans out/")
