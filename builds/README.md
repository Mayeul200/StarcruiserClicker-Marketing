# Builds prêts à uploader

| Fichier | Taille | Plateformes cibles | Contenu |
|---|---|---|---|
| `starcruiser-clicker-itch.zip` | ~10 Mo | itch.io, GameJolt, CrazyGames, Poki, Newgrounds | Jeu complet (143 fichiers), `game.html` à la racine, sans .git/tools/server |

## Régénérer le zip (depuis le dépôt du jeu, branche main à jour) :
```bash
cd ../Starcruiser-Clicker
git archive --format=zip -o /tmp/sc.zip HEAD
# puis nettoyer : exclure .git/, tools/, server/, out/, node_modules/, .github/
```

## Fichier à lancer dans l'iframe : `game.html`

## Zip special itch.io (landing + JOUER -> site officiel)
`starcruiser-clicker-itch.zip` est genere par `builds/make-itch-zip.py` :
- main file itch.io = `index.html` (par defaut) : le joueur tombe sur la landing
- dans CE zip uniquement, tous les boutons JOUER de la landing pointent vers
  `https://starcruiserclicker.com/game.html?utm_source=itchio` en `target="_blank"`
- le site officiel (starcruiserclicker.com) n'est PAS modifie

Regenerer apres chaque changement du jeu : `python3 builds/make-itch-zip.py`

## Zip plateformes strictes (CrazyGames, Poki, GameJolt, Newgrounds)
`starcruiser-clicker-platforms.zip` = build BRUT (non patché) : main file = **`game.html`**,
le jeu est jouable directement dans l'iframe de la plateforme (exigé par CrazyGames).
Le bouton "Site officiel" dans la topbar du jeu (visible uniquement sur ces domaines)
renvoie vers `https://starcruiserclicker.com/game.html?utm_source=embed`.

## Re-publication (mise à jour des plateformes existantes)
1. Régénérer les zips après chaque changement du jeu : `python3 builds/make-itch-zip.py` et `python3 builds/make-platforms-zip.py`
2. **itch.io** : remplacer le fichier sur la MÊME page projet (ne PAS recréer de page, sinon pénalité)
3. **CrazyGames / GameJolt / Poki / Newgrounds** : re-upload le zip `starcruiser-clicker-platforms.zip` (ou les fichiers dézippés) sur la même fiche jeu
4. Le bouton « Site officiel » renvoie vers starcruiserclicker.com (utm_source=embed) ; sur itch.io la landing renvoie via JOUER (utm_source=itchio)
