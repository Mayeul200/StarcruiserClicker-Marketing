#!/usr/bin/env python3
"""Génère un lot de fiches de posts à partir de la bibliothèque d'idées.

Pioche des idées dans content/ideas.json (sans répéter celles déjà utilisées),
remplit le template templates/fiche-post.md et écrit les fiches dans content/postes/.

Exemple :
    python scripts/generate_batch.py --count 4
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDEAS_PATH = ROOT / "content" / "ideas.json"
TEMPLATE_PATH = ROOT / "templates" / "fiche-post.md"
OUTPUT_DIR = ROOT / "content" / "postes"

FORMAT_LABELS = {
    "format_main": ("🎬", "Vidéo principale"),
    "format_mecanique": ("⚙️", "Mécanique"),
}

# La vidéo principale d'abord, puis les mécaniques dans l'ordre défini


def load_ideas() -> dict:
    with open(IDEAS_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_ideas(ideas: dict) -> None:
    with open(IDEAS_PATH, "w", encoding="utf-8") as f:
        json.dump(ideas, f, indent=2, ensure_ascii=False)
        f.write("\n")


def pick_ideas(ideas: dict, count: int) -> list[dict]:
    """Vidéo principale d'abord, puis les mécaniques dans l'ordre du fichier."""
    available = {k: [i for i in v if not i.get("used")] for k, v in ideas.items()}
    total = sum(len(v) for v in available.values())
    if total == 0:
        sys.exit("Erreur : plus aucune idée disponible dans content/ideas.json. "
                 "Ajoute de nouvelles idées ou réinitialise 'used'.")
    if count > total:
        print(f"⚠️ Seulement {total} idées disponibles ; demande de {count}.")
        count = total

    ordered: list[tuple[str, dict]] = []
    for key in ("format_main", "format_mecanique"):
        for idea in available.get(key, []):
            ordered.append((key, idea))
    return [{"key": k, "idea": i} for k, i in ordered[:count]]


def next_dates(count: int) -> list[str]:
    """Un créneau par jour, à partir de demain (cadence : 1 vidéo/jour)."""
    today = date.today()
    return [(today + timedelta(days=i + 1)).isoformat() for i in range(count)]


def render(template: str, key: str, idea: dict, date_prevue: str) -> str:
    letter, label = FORMAT_LABELS[key]
    replacements = {
        "{{ format }}": f"{letter} — {label}",
        "{{ hook }}": idea["hook"],
        "{{ description }}": idea["description"],
        "{{ cta }}": idea["cta"],
        "{{ hashtags }}": idea["hashtags"],
        "{{ sequence }}": idea["sequence"],
        "{{ date_prevue }}": date_prevue,
        "{{ duree }}": idea.get("duration", "20"),
        "{{ shoot_notes }}": idea.get("shoot_notes", ""),
    }
    for k, v in replacements.items():
        template = template.replace(k, v)
    return template


def main() -> None:
    p = argparse.ArgumentParser(description="Génère un lot de fiches de posts")
    p.add_argument("--count", type=int, default=4, help="Nombre de posts à générer")
    a = p.parse_args()

    ideas = load_ideas()
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    picked = pick_ideas(ideas, a.count)
    dates = next_dates(len(picked))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for item, date_prevue in zip(picked, dates):
        fiche = render(template, item["key"], item["idea"], date_prevue)
        out = OUTPUT_DIR / f"{item['idea']['id']}-{date_prevue}.md"
        out.write_text(fiche, encoding="utf-8")
        for group in ideas.values():
            for i in group:
                if i["id"] == item["idea"]["id"]:
                    i["used"] = True
                    i["published_at"] = None
        print(f"📝 Fiche générée : content/postes/{out.name}")

    save_ideas(ideas)
    print(f"✅ {len(picked)} fiches générées. Idées marquées comme utilisées.")


if __name__ == "__main__":
    main()
