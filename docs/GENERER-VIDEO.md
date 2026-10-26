# Générer la vidéo 1 sur ton PC (2 minutes)

Le montage tourne dans la sandbox Vibe, mais la vidéo finale (7,6 Mo) n'est pas
versionnée dans le repo (`out/` est dans `.gitignore`). Pour la générer chez toi :

## 1. Prérequis : Python 3.10+

Vérifie : `python --version` (ou `python3 --version`)

## 2. Installer les dépendances (une seule fois)

```bash
pip install imageio-ffmpeg pillow matplotlib
```

C'est tout — le binaire FFmpeg est inclus dans `imageio-ffmpeg`, rien d'autre à installer.

## 3. Générer la vidéo

```bash
cd StarcruiserClicker-Marketing
python scripts/make_trailer.py
```

La vidéo sort dans **`out/main-trailer.mp4`** (1080×1920, ~21,5 s, ~7,6 Mo).

## 4. Publier

- **YouTube Studio** → Importer → `out/main-trailer.mp4`
- **TikTok Studio** → Upload → `out/main-trailer.mp4`

Descriptions prêtes : voir la fiche `content/postes/main-*.md` ou la conversation.

## Remarque

`scripts/make_trailer.py` contient le plan de montage (clips, durées, overlays).
Pour changer l'accroche : modifier `HOOK_LINES` en haut du script et relancer.
