# Checklist — soumission sur les plateformes d'hébergement

Lien à utiliser partout : `https://starcruiserclicker.com/?utm_source=<plateforme>`

## itch.io ✅ PUBLIÉ
- [x] Compte créé, page projet « HTML5 / playable in browser »
- [ ] Titre + tagline + descriptions (voir `content/itch-io.md`)
- [ ] 5–8 captures 1280×720 + 1 GIF animé (boucle décollage)
- [ ] Prix : Name your price (0 par défaut)
- [ ] Tags : idle, incremental, clicker, space, browser-game, free, pwa
- [ ] Liens : site, wiki, devlog, leaderboard
- [ ] Commentaires activés

## CrazyGames (STRICT : jeu jouable dans l'iframe obligatoire)
- [ ] Compte dev + soumission
- [ ] Utiliser `builds/starcruiser-clicker-platforms.zip` (build brut, PAS le zip itch patché)
- [ ] Main file = **`game.html`** — le jeu doit tourner chez eux, pas de redirection
- [ ] Le funnel vers ton site passe par le bouton "Site officiel" en topbar (auto sur crazygames.com)
- [ ] Icône 512×512, bannière, description EN
- [ ] UTM `?utm_source=crazygames`

## GameJolt
- [ ] Page jeu + widget jouable en ligne
- [ ] Devlog lié à actualites.html
- [ ] UTM `?utm_source=gamejolt`

## Poki
- [ ] Formulaire de soumission rempli (build HTML5)
- [ ] UTM `?utm_source=poki`

## Newgrounds
- [ ] Upload du jeu + portail « Games »
- [ ] UTM `?utm_source=newgrounds`

## Google Search Console
- [ ] Propriété vérifiée sur starcruiserclicker.com
- [ ] sitemap.xml soumis
- [ ] Indexation demandée : /, /guide.html, /en/, /game.html

## Awesome lists / annuaires
- [ ] PR `leereilly/games` (texte dans `pr-awesome-lists.md`)
- [ ] PR awesome-html5-games actif
- [ ] Fiche AlternativeTo (alternative à Cookie Clicker)
- [ ] Annuaire FR : jeuxweb.fr, Top Jeux Gratuits

## Suivi
Reporter chaque soumission + date + statut dans `docs/KPI.md` (tableau hebdo),
colonne « Sessions jeu » par utm_source pour mesurer ce qui rapporte vraiment.
