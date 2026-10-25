# [{{ format }}] {{ hook }}

**Statut :** 📝 à valider
**Date prévue :** {{ date_prevue }}
**Durée cible :** {{ duree }} s
**Plateformes :** YouTube Shorts, TikTok
**Séquence source :** `assets/sequences/{{ sequence }}`

## Accroche (hook)

{{ hook }}

## Description

{{ description }}

## CTA

{{ cta }}

## Hashtags

{{ hashtags }}

## Plans à filmer

{{ shoot_notes }}

## Checklist production

- [ ] Séquence enregistrée et propre
- [ ] Vidéo montée : `python scripts/build_video.py --input assets/sequences/{{ sequence }} --hook "{{ hook }}" --cta "{{ cta }}" --duration {{ duree }}`
- [ ] Lien avec UTM correct
- [ ] Fiche validée par un humain
- [ ] Publiée sur YouTube Shorts (`?utm_source=youtube`)
- [ ] Publiée sur TikTok (`?utm_source=tiktok`)
- [ ] KPI récupérés dans `docs/KPI.md`
