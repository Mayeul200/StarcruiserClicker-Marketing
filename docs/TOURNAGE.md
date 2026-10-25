# Guide de tournage — Starcruiser Clicker

Ce document explique **exactement quoi enregistrer, comment et où le mettre**.

## Où mettre les fichiers

```
assets/sequences/<nom>.mp4
```

Noms attendus (définis dans `content/ideas.json`) :

| Fichier | Contenu |
|---|---|
| `main-trailer.mp4` | Vidéo principale (best-of, 30 s) |
| `mecanique-clics.mp4` | La pièce dorée + achats |
| `mecanique-batiments.mp4` | Les 14 bâtiments |
| `mecanique-fusee.mp4` | Assemblage de la fusée |
| `mecanique-voyage.mp4` | Décollage + cinématique de voyage |
| `mecanique-cometes.mp4` | Interception de comètes |
| `mecanique-contrats.mp4` | Contrats express 30 s |
| `mecanique-cartes.mp4` | Boosters + collection |
| `mecanique-atelier.mp4` | Poussière d'Étoiles + Atelier Galactique |
| `mecanique-classement.mp4` | Classement + Radar de pilote |

## Comment enregistrer

1. **Ouvre le jeu** sur [starcruiserclicker.com](https://starcruiserclicker.com) (ou en local) et passe en **plein écran** (F11) pour un rendu propre.
2. **Outil d'enregistrement d'écran** :
   - Windows : `Win + G` (barre Xbox Game Capture) → Enregistrer.
   - macOS : `Cmd + Maj + 5` → Enregistrement d'écran.
   - Alternative : OBS Studio (gratuit) qui permet aussi d'enregistrer en vertical directement.
3. **Format** : enregistre en **paysage, en 1080p minimum**. Le script `build_video.py` recadre en vertical 1080×1920 automatiquement — mais tu peux aussi enregistrer directement une fenêtre de jeu au format vertical si tu préfères cadrer toi-même.
4. **Durée brute** : 30–60 s par séquence — on coupera à 15–25 s au montage.
5. **Pas besoin de son** : le montage ajoute du texte ; la musique se choisit à la publication (musique tendance de la plateforme).

## Quoi filmer, séquence par séquence

### 🎬 `main-trailer.mp4` — LA vidéo principale
Un best-of de tout le jeu, dans cet ordre :
1. **2 s** — clics sur la pièce dorée (avec les `+X` qui volent)
2. **3 s** — achat en rafale de bâtiments, compteur de production qui grimpe
3. **5 s** — assemblage de la fusée pièce par pièce (accéléré)
4. **5 s** — décollage + cinématique de voyage
5. **5 s** — une comète interceptée au missile
6. **5 s** — ouverture d'un booster de cartes
7. **5 s** — arrivée sur une destination lointaine (ex. Andromède)
8. Finir sur le logo / l'écran du jeu avec le nom visible.

Astuce : filme chaque étape séparément dans des takes courts, puis assemble-les dans l'ordre avec le paramètre `--sections` ou en les collant avant le montage.

### ⚙️ Les 9 vidéos « mécanique »
Une vidéo = **une mécanique présentée de bout en bout**. Le détail de chaque plan est dans le champ `shoot_notes` de `content/ideas.json` (fichier, durée cible, plans attendus). En résumé :

- **Clics** : gros plan pièce dorée → clics rapides → premier bâtiment acheté → production auto.
- **Bâtiments** : défilement des 14 bâtiments, achat en rafale, production/s qui explose.
- **Fusée** : achat des 10 pièces une par une (accéléré), fusée complète.
- **Voyage** : pad → décollage → cinématique → nouvelle planète → bonus permanent → expédition suivante.
- **Comètes** : arrivée comète → visée missile → interception ×2-3.
- **Contrats** : acceptation → minuteur → clics frénétiques → objectif atteint.
- **Cartes** : ouverture booster → révélation des cartes → collection → bonus.
- **Atelier** : fin d'expédition → Poussière d'Étoiles → améliorations achetées → run suivant plus fort.
- **Classement** : écran classement → Radar de pilote → records auto.

### Astuces de tournage
- Pour les mécaniques tardives (Forge du Vide, Virgo, Andromède) : utilise une **save avancée** ou le mode infini pour accéder aux contenus rapidement plutôt que de jouer des heures.
- Nettoie l'écran avant d'enregistrer : ferme les popups, masque le curseur système si possible (OBS le permet).
- Filme 2-3 takes de chaque action, garde le meilleur.

## Après le tournage : montage

```bash
# Une vidéo mécanique (20 s) :
python scripts/build_video.py \
  --input assets/sequences/mecanique-clics.mp4 \
  --hook "This golden part funds your entire space program 💰" \
  --cta "Play for free: starcruiserclicker.com" \
  --duration 20 \
  --output out/mecanique-clics.mp4

# La vidéo principale (30 s) :
python scripts/build_video.py \
  --input assets/sequences/main-trailer.mp4 \
  --hook "One click. One galaxy. How far can you go? 🚀" \
  --cta "Play for free: starcruiserclicker.com" \
  --duration 30 \
  --output out/main-trailer.mp4
```

Puis publication manuelle sur YouTube Shorts + TikTok avec la description de la fiche correspondante (`content/postes/`).

## Ordre de publication (1 vidéo/jour)

| Jour | Vidéo |
|---|---|
| J1 | 🎬 **Principale** — le trailer best-of |
| J2 | ⚙️ Clics |
| J3 | ⚙️ Bâtiments |
| J4 | ⚙️ Fusée |
| J5 | ⚙️ Voyage |
| J6 | ⚙️ Comètes |
| J7 | ⚙️ Contrats |
| J8 | ⚙️ Cartes |
| J9 | ⚙️ Atelier Galactique |
| J10 | ⚙️ Classement |

Ensuite : réutiliser les séquences pour des variantes d'accroches (le montage s'adapte, seul le hook change), jusqu'à épuisement des idées dans `content/ideas.json`. La vidéo principale peut aussi être re-publiée avec une autre accroche après 2-3 semaines.
