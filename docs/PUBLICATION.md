# Publication programmée — la méthode 100 % gratuite

Pas besoin d'outil payant : **YouTube et TikTok intègrent nativement la programmation de Shorts/vidéos**, gratuitement. On charge les 10 vidéos une fois, on les programme 1/jour, et c'est tout.

> ℹ️ Pourquoi pas Postiz ? Postiz Cloud n'a pas d'offre gratuite permanente (essai 7 jours, puis à partir de 29 $/mois). Le self-host est gratuit en licence mais demande un VPS (~5 €/mois) et la validation de tes propres apps développeur YouTube/TikTok (plusieurs semaines). La programmation native fait le même travail pour zéro euro.

## 1. YouTube Shorts — programmation native (gratuite)

Prérequis : une chaîne YouTube (création gratuite) vérifiée par SMS (nécessaire pour les uploads longs, recommandé dans tous les cas).

1. Va sur [studio.youtube.com](https://studio.youtube.com) → **Créer → Importer des vidéos**.
2. Téléverse `out/main-trailer.mp4`.
3. Remplis titre, description et tags depuis la fiche correspondante (`content/postes/`), avec le lien `https://starcruiserclicker.com/?utm_source=youtube` en première ligne de description.
4. Dans **Visibilité** : choisis **Planifier** → date et heure (garde la même heure chaque jour, ex. 18h00).
5. Coche « Non, ce n'est pas un contenu conçu pour les enfants ».
6. Répète pour les 10 vidéos : tout se téléverse en une session, chacune planifiée sur son jour.

Vérifie ensuite dans **Contenu → À venir** que les 10 vidéos sont bien en file.

## 2. TikTok — programmation native (gratuite)

Prérequis : un compte TikTok (passe-le en **compte Pro** dans Paramètres → Gérer le compte, gratuit — débloque les statistiques).

1. Va sur [tiktok.com](https://www.tiktok.com) connecté à ton compte → bouton **Upload** (ou Studio TikTok : [tiktok.com/tiktokstudio](https://www.tiktok.com/tiktokstudio)).
2. Téléverse la vidéo **en vertical** (nos vidéos sortent déjà en 1080×1920 via `build_video.py`).
3. Remplis la légende depuis la fiche : accroche + `#hashtags` + `Play free: starcruiserclicker.com/?utm_source=tiktok`.
4. Dans **Paramètres avancés** → **Programmer** : choisis la date et l'heure (TikTok permet de programmer jusqu'à 10 jours à l'avance — parfait pour nos 10 jours).
5. Répète pour les 10 vidéos en une session.

À noter : TikTok propose la programmation jusqu'à 10 jours à l'avance, donc les 10 vidéos de la série se programment en une seule fois.

## 3. Bien préparer les vidéos avant l'upload

- YouTube Shorts : ≤ 60 s et format vertical (9:16) — nos vidéos montées sont déjà conformes (1080×1920, 15–30 s).
- TikTok : ≤ 10 min, vertical. Conforme aussi.
- La **musique** : ajoute-la au moment de l'upload si tu veux un son tendance (les deux plateformes proposent des sons libres de droits à l'upload). La vidéo montée n'a pas de musique — c'est voulu, pour rester flexible.
- La **miniature** : TikTok la choisit automatiquement ; sur YouTube tu peux en importer une (les 10 vidéos ont l'outro « Starcruiser Clicker » comme dernière image, qui fait une bonne miniature).

## 4. Rappel du flux complet

```
1. Filmer 10 séquences         (docs/TOURNAGE.md)          ~2 h
2. Monter via build_video.py   (docs/TOURNAGE.md §montage) ~30 min
3. Upload + programmer YouTube (ci-dessus §1)               ~30 min
4. Upload + programmer TikTok  (ci-dessus §2)               ~30 min
5. Suivre les KPI chaque semaine (docs/KPI.md)
```

En une demi-journée de travail, tes 10 pubs sont filmées, montées et programmées pour les 10 prochains jours — sans abonnement, sans VPS, sans API à valider.

## 5. Et si un jour tu veux plus ?

- **V2 possible plus tard** : script d'upload automatique YouTube via leur API officielle dans GitHub Actions (gratuit, mais l'app Google doit passer en production → validation). TikTok reste manuel (leur API vidéo exige une app validée).
- Pour 10 vidéos/mois, la programmation native suffit largement. On réévaluera si la stratégie passe à plusieurs posts/jour ou à plus de réseaux.
