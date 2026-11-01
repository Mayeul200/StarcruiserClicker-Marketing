# Plan d'acquisition — hors réseaux sociaux classiques

Objectif : faire connaître Starcruiser Clicker par le plus de canaux possibles,
**en complément** des réseaux sociaux (YouTube Shorts / TikTok / Instagram déjà en
cours — voir `PLAN-PUBLICATION.md`). Zéro budget, 100 % organique + communautés.

Lier du jeu : toujours avec un paramètre UTM (voir `docs/KPI.md` §2), ex. :
`https://starcruiserclicker.com/?utm_source=itch.io`

---

## 1. Plateformes d'hébergement de jeux (levier n°1)

| Plateforme | Pourquoi | Action | UTM |
|---|---|---|---|
| **itch.io** | Communauté web games très active, gratuit, « name your price » | Fiche jeu complète (voir `content/itch-io.md`), build « playable in browser », 5 captures + GIF du décollage, tags `#idle #incremental #space #clicker` | `?utm_source=itchio` |
| **CrazyGames** | Gros trafic HTML5 | Soumettre le build web tel quel via leur portail dev | `?utm_source=crazygames` |
| **GameJolt** | Communauté indie engagée, bons retours | Page jeu + devlog synchronisé avec `actualites.html` | `?utm_source=gamejolt` |
| **Poki** | Distribution massive | Soumission via formulaire dev | `?utm_source=poki` |
| **Newgrounds** | Audience historique jeux web/clickers | Upload + portail | `?utm_source=newgrounds` |

Checklist soumissions : voir `content/checklist-plateformes.md`.

## 2. Reddit (communautaire, pas de spam)

- Subs cibles : `r/incremental_games`, `r/WebGames`, `r/idle_games`, `r/IndieGaming` (Showoff Saturday uniquement), `r/gamedev` (post technique : WASM + anti-triche leaderboard).
- Format : 1 post/semaine max, titre accrocheur, GIF, lien UTM reddit, **répondre à tous les commentaires dans l'heure** (crucial pour l'algo).
- Post type rédigé : `content/post-reddit.md`.

## 3. SEO & backlinks gratuits

- **Google Search Console** : soumettre `sitemap.xml`, demander l'indexation de `/`, `/guide.html`, `/en/`. Le wiki sert directement le référencement.
- Mots-clés cibles : « clicker spatial », « jeu incrémental français », « idle game space », « incremental game rocket ».
- **Awesome lists GitHub** : PR dans `awesome-html5-games`, `awesome-indie-games`, `awesome-clicker-games` → backlink fort. Texte de PR : `content/pr-awesome-lists.md`.
- **AlternativeTo** : fiche « alternative à Cookie Clicker / Adventure Capitalist ».
- Annuaire FR : jeuxweb.fr, Top Jeux Gratuits, etc.

## 4. Presse & créateurs (gratuit)

- YouTubeurs/TikTokers niche idle/clicker (10k–100k abonnés) : mail-type dans `content/mail-youtubeurs.md`, proposer preview + honest review.
- Sites : IndieDB (page + news), TIGSource, Rock Paper Shotgun (tips), JeuxVideo.com (forum).
- Newsletters : Indie Game Newsletter, WebGame Weekly.

## 5. Communautés Discord & forums

- Discord r/incremental_games, serveurs FR dev indé, « Incremental Games » community.
- Forums : TIGSource, GameDev.net, forums clickers.

## 6. Viralité mécanique dans le jeu

- Bouton « Partager mon record » (Web Share API) avec lien pré-rempli : « J'ai atteint Mars sur Starcruiser Clicker 🚀 ».
- Le nom d'entreprise spatiale visible sur `records.html` incite au partage pour grimper au classement.

## 7. Cross-promotion

- Bannière/lien mutuel avec 2–3 autres jeux web indé (« jeux similaires »).
- Événement conjoint avec un créateur de contenu.

## 8. Game jams & concours

- Participer à une jam itch.io (même post-launch : « jam edition »).
- Concours de record annoncé sur `records.html` (ex. record mondial le plus haut à date fixe).

## 9. Mesure & boucle

- Umami déjà en place : suivre les sessions par `utm_source` (itchio, reddit, crazygames, poki…).
- KPI hebdo (`docs/KPI.md`) : sessions de jeu par canal, conversion lien→partie, rétention J1/J7.
- Chaque dimanche : réaffecter l'effort vers les 2 meilleurs canaux.

---

## Calendrier prioritaire (4 semaines)

| Semaine | Actions |
|---|---|
| **S1** | itch.io + GameJolt + CrazyGames soumis · 1 post Reddit bien placé · Google Search Console (sitemap + indexation) |
| **S2** | PR awesome-lists GitHub · AlternativeTo · 3 youtubeurs contactés · 2–3 communautés Discord |
| **S3** | Poki + Newgrounds · annuaires FR · bouton « partager mon record » dans le jeu (petit dev) |
| **S4** | Bilan KPI · réaffectation · concours de record · cross-promo avec un autre jeu web |
