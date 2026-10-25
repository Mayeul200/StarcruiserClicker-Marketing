# Stratégie marketing — Starcruiser Clicker

Objectif : transformer des inconnus en joueurs. Pas seulement des vues — des sessions de jeu réelles sur [starcruiserclicker.com](https://starcruiserclicker.com).

## 1. Positionnement

**Starcruiser Clicker** est un clicker spatial jouable immédiatement, gratuitement, dans le navigateur. On ne promet pas un jeu futur : on montre du vrai gameplay, des progressions spectaculaires et des destinations cosmiques.

Ton de marque : émerveillement spatial + satisfaction de progression (idle/clicker). Posts en anglais pour une audience internationale.

## 2. Réseaux — priorités

| Réseau | Rôle | Effort |
|---|---|---|
| **YouTube Shorts** | Priorité n°1 : découverte organique, visibilité durable | Faible–moyen (automatisable) |
| **TikTok** | Laboratoire d'accroches virales (mêmes vidéos) | Moyen |
| **Reddit** | Vrais joueurs + retours (r/incremental_games, r/idleGames, r/ClickerGames…) | Humain uniquement |
| **X** | Visibilité devs/créateurs : GIFs, updates dev | Faible |

On ne disperse pas : **YouTube Shorts + TikTok d'abord** (mêmes vidéos verticales), Reddit en complément humain.

## 3. Formats de contenu

Répartition de test sur le premier mois :

| Format | Part | Description |
|---|---|---|
| **A — Progression spectaculaire** | 50 % | Accélération du début vers une destination lointaine. « How far can you go with just one click? » (15–20 s) |
| **B — Plaisir d'optimisation** | 25 % | Une petite amélioration → industrie spatiale entière. « From one click to an entire space industry. » |
| **C — Révélation cosmique** | 15 % | Visuel fort (Andromède, trou noir, centre galactique) → gameplay réel. « Your next destination is 2.5 million light-years away. » |
| **D — Coulisses dev** | 10 % | Avant/après, choix de design, question à la communauté. « I built a space clicker game. Here's what happens when you reach Andromeda. » |

Ce sont des proportions de test, pas une formule garantie. Elles s'ajustent selon les KPI (`docs/KPI.md`).

## 4. Pipeline de production

1. **Bibliothèque de séquences** — enregistrer une fois des screencasts propres : clics, achats, accélérations, destinations, effets. Matière première de dizaines de vidéos (`assets/sequences/`).
2. **Génération des concepts** — l'IA pioche une séquence, propose 5 accroches, rédige la description, choisit le format. Anti-doublon via `content/ideas.json`.
3. **Montage automatique** — `scripts/build_video.py` (FFmpeg) : crop vertical 1080×1920, accroche en haut, sous-titres, outro avec le nom du jeu.
4. **Programmation** — GitHub Actions produit les lots (`content-pipeline.yml`). Publication API directe seulement si les autorisations existent ; sinon lot prêt à publier manuellement.
5. **Analyse hebdo** — récupération des métriques accessibles, comparaison accroches/formats, recommandations (prompt `prompts/analyse-hebdo.md`).

## 5. Automatisation : ce qui est automatisable

| Fonction | Faisabilité | Décision |
|---|---|---|
| Publier à heure fixe | Très bonne | Automatisé (API ou lot manuel) |
| Générer textes/visuels | Très bonne | Automatisé |
| Répondre aux commentaires reçus | Selon réseau/autorisation | Réponse préparée par IA, **validation humaine** |
| Répondre à des inconnus pour attirer des abonnés | Risqué, parfois interdit | **Interdit** |
| Analyser et adapter | Bonne | Automatisé (rapport hebdo) |
| Compte sans surveillance | Possible mais risqué | **Non** : validation humaine de chaque publication |

### Limites des API (à vérifier avant de coder)

- **YouTube** : upload via YouTube Data API (application OAuth + écran de consentement à configurer).
- **TikTok** : Content Posting API, application enregistrée + autorisations requises.
- **X** : publication automatisée possible sous conditions ; bots de réponse IA nécessitent une autorisation écrite explicite.
- **Instagram** : publication + gestion des commentaires sur comptes pro autorisés.

Règle de sécurité : jamais de script qui pilote l'interface du réseau pour simuler un utilisateur.

### Secrets

Clés API uniquement dans **GitHub → Settings → Secrets and variables → Actions**. Jamais dans le code ou un fichier versionné.

## 6. Règles

- Toujours du **vrai gameplay** ; ne jamais présenter une fonctionnalité inexistante.
- Liens avec paramètres de suivi : `?utm_source=youtube`, `?utm_source=tiktok`.
- Pas de publicité payante avant d'avoir identifié un format qui attire régulièrement des joueurs.
- Pas de commentaires/réponses artificiels pour simuler une communauté.

## 7. Feuille de route

| Version | Contenu | État |
|---|---|---|
| **V1** | Post généré tous les 2 jours, publié automatiquement, historique anti-doublon | ✅ Ce dépôt |
| **V2** | Récupération des commentaires, réponses IA préparées, validation humaine | ⬜ |
| **V3** | Analyse des stats, choix des sujets performants, adaptation progressive | ⬜ |
