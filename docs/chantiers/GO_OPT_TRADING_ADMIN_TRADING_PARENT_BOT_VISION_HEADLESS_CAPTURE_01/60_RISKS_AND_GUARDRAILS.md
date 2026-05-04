---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01_RISKS
doc_type: risks_guardrails
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01
status: open
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 60_RISKS_AND_GUARDRAILS

## Risques

### R1: Secrets / cookies / sessions

- **Risque**: TradingView/Coinglass peut necessiter authentification
- **Mitigation**: 
  - Utiliser URLs publiques sans login si possible (ex: graphiques embed)
  - Si login requis: stocker cookies dans fichier separe hors repo
  - Ne jamais commiter de cookies/sessions dans le repo
  - Utiliser profil Chromium isole (~/.cache/bot_vision_headless/)

### R2: Fichiers 0-byte / partiels

- **Risque**: Crash PIL dans desk_bridge
- **Mitigation**: Atomic write (.uploading -> rename) + verification taille > 0
- **Deja applique**: GO_VISION_INBOX_REPAIR_01 a nettoye les inputs corrompus

### R3: Charge CPU/RAM

- **Risque**: Chromium headless ~150 MB RAM, CPU pic pendant capture
- **Mitigation**: 
  - Oneshot timer (pas de daemon permanent)
  - Timeout capture 30s
  - max 1 instance a la fois (pas de parallele)

### R4: Faux positifs

- **Risque**: Erreur reseau, page non chargee -> screenshot vide/blanc
- **Mitigation**: Verifier taille > seuil minimal (ex: > 50 KB) avant rename

### R5: Trading reel involontaire

- **Risque**: AUCUN — bot_vision_headless ne fait que de la capture visuelle
- **Mitigation**: Le mode PAPER de Desk Pro est preserve

### R6: Dependance Playwright/Chromium

- **Risque**: Version chromium instable, crash
- **Mitigation**: Chromium installe via Playwright (version testee), pas le chromium systeme

### R7: Conflit avec ShareX existant

- **Risque**: Deux sources ecrivent dans vision_inbox
- **Mitigation**: 
  - Nommage unique avec timestamp + random
  - vision_bot traite les fichiers sequentiellement
  - ShareX peut etre desactive si capture headless stable

## Garde-fous automatiques

| Garde-fou | Ou | Quand |
| --- | --- | --- |
| `[ -s "$file" ]` | bridge script | Avant Image.open() |
| Atomic write | capture script | Ecriture vision_inbox |
| Timeout 30s | capture script | Page load + screenshot |
| Cleanup tmp | capture script | Apres chaque cycle |
| Cleanup .uploading > 5 min | capture script | Debut de chaque cycle |
| Exit 0 si inbox vide | bridge script | Deja implemente |
