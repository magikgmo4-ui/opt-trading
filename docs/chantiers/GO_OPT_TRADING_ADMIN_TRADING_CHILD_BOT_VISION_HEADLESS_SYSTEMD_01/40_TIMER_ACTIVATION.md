---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01_ACTIVATION
doc_type: timer_activation
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_TIMER_ACTIVATION

## Commande

```bash
sudo systemctl enable --now bot-vision-headless-capture.timer
```

## Resultat

**PASS** — Timer enabled + active.

## Etat

| Propriete | Valeur |
| --- | --- |
| is-enabled | enabled |
| is-active | active |
| Next trigger | 2026-05-04 17:39 EDT (~9 min) |
| Intervalle | 10 min |
| Jitter | 30s randomized |
| Triggers | bot-vision-headless-capture.service (succes confirmes) |

## Verification

```
bot-vision-headless-capture.timer bot-vision-headless-capture.service
Mon 2026-05-04 17:28:49 EDT  Mon 2026-05-04 17:28:49 EDT  bot-vision-headless-capture
```

## Premier cycle automatique

Le timer a deja declenche une premiere fois lors du `enable --now`.
Prochain declenchement automatique dans ~9 minutes.
Tous les cycles produiront:
- 1 PNG + 1 JSON par capture
- Ecriture atomique (.uploading -> rename)
- Traitement par vision_bot (OCR)
- Traitement par desk_bridge (crop 2x2)

## RISKS

- À qualifier.
