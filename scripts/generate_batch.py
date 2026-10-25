#!/usr/bin/env python3
"""Génère un lot de fiches de posts à partir de la bibliothèque d'idées.

Pioche des idées dans content/ideas.json (sans répéter celles déjà utilisées),
remplit le template templates/fiche-post.md et écrit les fiches dans content/postes/.

Exemple :
    python scripts/generate_batch.py --count 4
"""

import argparse
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDEAS_PATH = ROOT / "content" / "ideas.json"
TEMPLATE_PATH = ROOT / "templates" / "fiche-post.md"
OUTPUT_DIR = ROOT / "content" / "postes"

FORMAT_LABELS = {
    "format_a_progression": ("A", "Progression"),
    "format_b_optimisation": ("B", "Optimisation"),
    "format_c_revelation": ("C", "Révélation"),
    "format_d_coulisses": ("D", "Coulisses"),
}

# Répartition de test : 50% A, 25% B, 15% C, 10% D
WEIGHTS = {"format_a_progression": 50, "format_b_optimisation": 25,
           "format_c_revelation": 15, "format_d_coulisses": 10}


def load_ideas() -> dict:
    with open(IDEAS_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_ideas(ideas: dict) -> None:
    with open(IDEAS_PATH, "w", encoding="utf-8") as f:
        json.dump(ideas, f, indent=2, ensure_ascii=False)
        f.write("\n")


def pick_ideas(ideas: dict, count: int) -> list[dict]:
    available = {k: [i for i in v if not i.get("used")] for k, v in ideas.items()}
    total = sum(len(v) for v in available.values())
    if total == 0:
        sys.exit("Erreur : plus aucune idée disponible dans content/ideas.json. "
                 "Ajoute de nouvelles idées ou réinitialise 'used'.")
    if count > total:
        print(f"⚠️ Seulement {total} idées disponibles ; demande de {count}.")
        count = total

    picked: list[tuple[str, dict]] = []
    keys = [k for k in available if available[k]]
    for _ in range(count):
        key = random.choices(keys, weights=[WEIGHTS[k] for k in keys])[0]
        idea = random.choice(available[key])
        picked.append((key, idea))
        available[key].remove(idea)
        if not available[key]:
            keys.remove(key)
    return [{"key": k, "idea": i} for k, i in picked]


def next_dates(count: int) -> list[str]:
    """Prochains créneaux : lundi, mercredi, vendredi, dimanche."""
    today = date.today()
    weekdays = [0, 2, 4, 6]
    slots = []
    d = today
    while len(slots) < count:
        if d.weekday() in weekdays and d >= today:
            slots.append(d.isoformat())
        d += timedelta(days=1)
    return slots


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
    }
    for k, v in replacements.items():
        template = template.replace(k, v)
    return template


def main() -> None:
    p = argparse.ArgumentParser(description="Génère un lot de fiches de posts")
    p.add_argument("--count", type=int, default=4, help="Nombre de posts à générer")
    p.add_argument("--seed", type=int, default=None, help="Seed aléatoire (reproductibilité)")
    a = p.parse_args()
    if a.seed is not None:
        random.seed(a.seed)

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
