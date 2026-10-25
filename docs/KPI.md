# KPI — Starcruiser Clicker

Principe : les vues ne garantissent pas des joueurs. On mesure avant tout les **clics vers le site** et les **sessions de jeu**.

## 1. Indicateurs

| Indicateur | Ce qu'il permet de comprendre | Source |
|---|---|---|
| Rétention de la vidéo (perte < 3 s) | L'accroche fonctionne-t-elle ? | YouTube Studio / TikTok Analytics |
| Partages et commentaires | Le contenu donne-t-il envie de réagir ? | Plateformes |
| **Clics vers le site** | La vidéo attire-t-elle de vrais visiteurs ? | Analytics du site (par `utm_source`) |
| **Sessions de jeu** | Les visiteurs jouent-ils réellement ? | Analytics du site |

## 2. Liens de suivi

Chaque lien contient un paramètre distinct par plateforme :

- YouTube : `https://starcruiserclicker.com/?utm_source=youtube&utm_medium=shorts`
- TikTok : `https://starcruiserclicker.com/?utm_source=tiktok&utm_medium=video`
- Reddit : `https://starcruiserclicker.com/?utm_source=reddit&utm_medium=post`
- X : `https://starcruiserclicker.com/?utm_source=x&utm_medium=post`

Outil d'analytics recommandé : respectueux de la vie privée (ex. Plausible, Umami, ou self-hosted).

## 3. Revue hebdomadaire

Chaque dimanche, remplir le tableau ci-dessous (à la main ou via le prompt `prompts/analyse-hebdo.md` alimenté par les données des plateformes) :

| Semaine | Post | Plateforme | Vues | Rétention 3 s | Clics site | Sessions jeu | Format |
|---|---|---|---|---|---|---|---|
| S1 | — | — | — | — | — | — | — |

Décisions attendues :
- Quel format (A/B/C/D) apporte le plus de **sessions de jeu** (pas seulement de vues) ?
- Quelle accroche retient au-delà de 3 secondes ?
- Doit-on ajuster les proportions des formats (`docs/STRATEGIE.md` §3) ?

## 4. Seuils de décision

- Un format qui, sur 4 vidéos, n'apporte aucune session → réduire sa part, réallouer au meilleur format.
- Un format reproductible qui apporte régulièrement des joueurs → **industrialiser** via le pipeline, envisager la publicité payante.
- Publicité payante : uniquement après identification d'un format gagnant organique.
