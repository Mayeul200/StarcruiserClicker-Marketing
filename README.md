# Starcruiser Clicker — Marketing

Système de marketing pour faire connaître **Starcruiser Clicker** ([starcruiserclicker.com](https://starcruiserclicker.com)), un clicker spatial où l'on construit sa fusée pour explorer l'espace.

Ce dépôt contient la stratégie, le calendrier éditorial, la bibliothèque d'idées de posts et un pipeline automatisé de production de contenu, piloté par GitHub Actions.

## Structure

```
docs/
  STRATEGIE.md          # Stratégie complète : réseaux, formats, objectifs
  CALENDRIER.md         # Calendrier éditorial (4 posts/semaine)
  KPI.md                # Indicateurs à suivre et comment les mesurer
content/
  postes/               # Fiches de posts prêtes à produire (1 fichier = 1 post)
  video-scripts/        # Scripts d'accroches (bank de hooks)
assets/
  sequences/            # Séquences de gameplay brutes (matière première des vidéos)
  fonts/                # Polices pour le montage
prompts/
  generateur-post.md    # Prompt IA : générer une fiche de post depuis une idée
  analyse-hebdo.md      # Prompt IA : analyse des performances de la semaine
scripts/
  build_video.py        # Montage vidéo : crop vertical, sous-titres, outro (FFmpeg)
  generate_batch.py     # Génère un lot de posts à partir de la bibliothèque d'idées
templates/
  fiche-post.md         # Template de fiche de post
.github/workflows/
  content-pipeline.yml  # Génère un lot de contenu 2x/semaine via GitHub Actions
```

## Démarrage rapide

### 1. Produire une vidéo Shorts/TikTok

Enregistre une séquence de gameplay (screencast, 30–60 s) et place-la dans `assets/sequences/`. Puis :

```bash
pip install -r requirements.txt
python scripts/build_video.py \
  --input assets/sequences/progression-mars.mp4 \
  --hook "One click. One galaxy. How far can you go? 🚀" \
  --cta "Play for free: starcruiserclicker.com" \
  --output out/short.mp4
```

Le script recadre en 1080×1920, ajoute l'accroche en haut, les sous-titres et l'outro avec le nom du jeu.

### 2. Générer un lot de posts

```bash
python scripts/generate_batch.py --count 4
```

Pioche des idées dans `content/ideas.json` (sans répéter), remplit les fiches via le template, et marque les idées comme utilisées.

### 3. Automatiser via GitHub Actions

Le workflow `.github/workflows/content-pipeline.yml` tourne deux fois par semaine (lundi et vendredi). Il génère un lot de fiches de posts et ouvre automatiquement une **issue de revue** avec le contenu à valider avant publication.

## Publication

- **YouTube Shorts + TikTok** : publie les vidéos depuis un lot validé. La publication API directe nécessite des applications enregistrées et des autorisations (voir `docs/STRATEGIE.md`).
- **Reddit** : interventions humaines uniquement, dans des communautés pertinentes.
- Les secrets (clés API éventuelles) vont dans **Settings → Secrets and variables → Actions**. Jamais dans le code.

## Règles de marque

- Ton : émerveillement spatial + satisfaction de progression (idle/clicker).
- Langue des posts : anglais (audience internationale), hashtags : `#IdleGame #IncrementalGame #IndieGame #Space`.
- Toujours montrer du **vrai gameplay** — jamais promettre une fonctionnalité inexistante.
- Chaque lien utilise un paramètre de suivi : `?utm_source=youtube` / `?utm_source=tiktok`.
