---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01_SCOPE
doc_type: systemd_scope
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_SYSTEMD_SCOPE

## Automatisation

| Aspect | Valeur |
| --- | --- |
| Service | bot-vision-headless-capture.service (oneshot) |
| Timer | bot-vision-headless-capture.timer (10 min) |
| Freq | OnUnitActiveSec=10min |
| Jitter | RandomizedDelaySec=30s |
| Boot delay | OnBootSec=2min |
| User | ghost |
| CPU nice | 5 |
| IO class | best-effort |
| Timeout | 120s |

## Frequence retenue

**10 minutes** avec 30s de jitter aleatoire.
Justification:
- desk_bridge tourne deja toutes les 10 minutes
- Une capture par cycle bridge est suffisante
- Ne pas descendre sous 5 min sans GO dedie

## Ce qui est automatise

- Capture headless Playwright/Chromium
- Ecriture atomique vers vision_inbox
- Sidecar JSON
- Compatible avec vision_bot + desk_bridge

## Ce qui ne l'est pas

- Changement de profil de capture
- Nettoyage des anciens fichiers (deja gere par vision_bot -> processed)
- Notification Telegram (deja gere par bot_vision_step2)
- Desk Pro run (manuel ou timer separe)

## RISKS

- À qualifier.
