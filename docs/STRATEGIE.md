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

Le contenu parle **du jeu lui-même** : une vidéo principale (trailer best-of) + une vidéo par mécanique.

| Vidéo | Description | Durée |
|---|---|---|
| **🎬 Principale** | Trailer best-of : clics, bâtiments, fusée, voyage, comète, carte, destination lointaine | 30 s |
| **⚙️ Clics** | La pièce dorée, les clics, le premier bâtiment, l'automatisation | 20 s |
| **⚙️ Bâtiments** | 14 bâtiments de l'Atelier à la Forge du Vide | 20 s |
| **⚙️ Fusée** | Assemblage des 10 pièces, +4 % de portée chacune | 20 s |
| **⚙️ Voyage** | Décollage, cinématique, nouvelle planète, bonus permanent | 25 s |
| **⚙️ Comètes** | Interception de comètes au missile, mini-jeux | 15 s |
| **⚙️ Contrats** | Contrats express 30 s | 15 s |
| **⚙️ Cartes** | Boosters, collection, bonus | 15 s |
| **⚙️ Atelier** | Poussière d'Étoiles, Atelier Galactique, améliorations permanentes | 20 s |
| **⚙️ Classement** | Classement mondial des pilotes, Radar de pilote | 15 s |

Cadence : **1 vidéo/jour** une fois la série créée. Après la série, on décline les **mêmes séquences avec de nouvelles accroches** (3-4 par séquence) plutôt que de tourner de nouvelles vidéos. Le détail des plans à filmer est dans `docs/TOURNAGE.md`.

## 4. Pipeline de production

1. **Bibliothèque de séquences** — 10 screencasts propres (1 principal + 9 mécaniques). Chaque séquence sert ensuite 3-4 fois avec des accroches différentes (`assets/sequences/`, guide complet dans `docs/TOURNAGE.md`).
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
| **V1** | 1 fiche vidéo/jour générée automatiquement, historique anti-doublon | ✅ Ce dépôt |
| **V2** | Récupération des commentaires, réponses IA préparées, validation humaine | ⬜ |
| **V3** | Analyse des stats, choix des sujets performants, adaptation progressive | ⬜ |
