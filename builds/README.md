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
