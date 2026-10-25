# Publication automatique avec Postiz — Guide pas-à-pas

Postiz ([github.com/gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app)) est un planificateur social media open-source : on y connecte YouTube et TikTok via leurs **API officielles**, on y charge les vidéos une seule fois, et il publie automatiquement au rythme choisi (1/jour pour nous).

## ⚠️ Prérequis : où l'héberger

Postiz est une application **Docker** (Node.js + Redis + MongoDB) : elle doit tourner sur un **serveur** en permanence. **Cloudflare Pages/Workers ne peut PAS l'héberger** (pas de Docker, pas de processus longs).

Options, de la plus simple à la plus souple :

| Option | Coût | Remarque |
|---|---|---|
| **Postiz Cloud (version gratuite)** | 0 € | Le plus simple : rien à héberger, tu crées juste un compte sur postiz.com. Limites : peu de comptes/connecteurs en free. Parfait pour tester. |
| **VPS petit** (OVH, Hetzner, Contabo) | ~4–7 €/mois | Self-host complet, illimité, tes données chez toi. Recommandé si le jeu grossit. |
| Ton PC | 0 € | Possible mais le PC doit rester allumé pour que les publications partent à l'heure. Déconseillé. |

Cloudflare reste utile quand même : **DNS + HTTPS** devant le VPS (voir §3).

## 1. Option la plus rapide : Postiz Cloud (0 €, 15 minutes)

1. Va sur [postiz.com](https://postiz.com) → **Sign up** (offre gratuite).
2. Dans le dashboard : **Channels → Add Channel → YouTube**.
3. Connecte le compte Google de ta chaîne YouTube du jeu, autorise l'accès.
4. **Channels → Add Channel → TikTok**, connecte le compte TikTok du jeu.
5. Tu es prêt : passe directement à la §4.

## 2. Option self-host sur un VPS (~1 heure)

### 2.1 Louer et préparer le VPS

```bash
# Sur le VPS (Ubuntu 24.04) :
apt update && apt upgrade -y
apt install -y docker.io docker-compose-v2
```

### 2.2 Installer Postiz

```bash
mkdir -p /opt/postiz && cd /opt/postiz
curl -o docker-compose.yml https://raw.githubusercontent.com/gitroomhq/postiz-app/main/docker-compose.yml
# Éditer docker-compose.yml : changer JWT_SECRET et changer les mots de passe Mongo/Redis
docker compose up -d
```

L'app écoute sur le port 5000 du VPS.

### 2.3 DNS et HTTPS via Cloudflare (tu as déjà Cloudflare)

1. Dans Cloudflare → DNS : ajoute un enregistrement **A** `postiz` → IP de ton VPS, proxy activé (nuage orange).
2. Cloudflare → SSL/TLS : mode **Flexible** ou **Full** sur ce sous-domaine.
3. Accès : `https://postiz.tondomaine.com`.
4. Optionnel mais recommandé : Cloudflare Access (免费) devant `/` pour que seul toi puisse ouvrir l'interface.

### 2.4 Créer les apps développeur (self-host uniquement)

Postiz en self-host utilise **tes propres** apps développeur (Postiz Cloud gère les siennes) :

- **YouTube/Google Cloud Console** : créer un projet → activer **YouTube Data API v3** → écran de consentement OAuth (type External) → credentials OAuth 2.0 (Web) → ajouter `https://postiz.tondomaine.com/integrations/social/youtube` en redirect URI. Ton compte doit être **testeur** de l'app tant qu'elle n'est pas validée par Google.
- **TikTok for Developers** : créer une app → activer **Content Posting API** → redirect URI `https://postiz.tondomaine.com/integrations/social/tiktok`. L'accès complet à la publication peut nécessiter une validation TikTok (compte pro requis).

Renseigner les clés dans Postiz : **Settings → Integrations**, puis connecter les chaînes.

## 3. Comment ça s'articule avec notre pipeline

```
GitHub Actions (quotidien, 18h)          Postiz                    Plateformes
┌──────────────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│ Génère la fiche du jour   │    │ Vidéos chargées     │    │ YouTube Shorts   │
│ (hook, CTA, hashtags)     │───▶│ une fois,           │───▶│ TikTok           │
│ Issue de revue à valider  │    │ programmées 1/jour  │    │ (publication auto│
└──────────────────────────┘    └─────────────────────┘    │  via API officielle)│
   Montage: build_video.py         Calendar intégré        └─────────────────┘
   (FFmpeg, local)                (publie tout seul)
```

- Le repo produit le **contenu et le montage** ; Postiz gère la **programmation et la publication**.
- Une fois tes 10 vidéos montées (`out/*.mp4`), tu les charges TOUTES dans Postiz en une session, tu les programmes J1→J10, et tu n'as plus rien à faire pendant 10 jours.

## 4. Après l'installation : charger la série

1. Dans Postiz → **Create post** → sélectionner YouTube + TikTok en même temps (le même post part sur les deux).
2. Uploader `out/main-trailer.mp4`, mettre le titre/description/hashtags de la fiche `content/postes/main-*.md` (ajouter `?utm_source=youtube` / `?utm_source=tiktok` dans la description selon la plateforme).
3. Définir la date/heure de publication (garder la même heure chaque jour, ex. 18h).
4. Répéter pour les 9 vidéos mécaniques, **Schedule** chacune sur son jour (J2→J10).
5. Vérifier chaque matin le premier jour que les publications partent bien (onglet **Queue**).

## 5. Checklist finale

- [ ] Compte Postiz créé (Cloud ou self-host installé)
- [ ] Chaîne YouTube connectée
- [ ] Compte TikTok (pro) connecté
- [ ] 10 vidéos montées via `scripts/build_video.py`
- [ ] 10 posts programmés dans Postiz (1/jour)
- [ ] Lien UTM présent dans chaque description
- [ ] KPI relevés chaque semaine dans `docs/KPI.md`
