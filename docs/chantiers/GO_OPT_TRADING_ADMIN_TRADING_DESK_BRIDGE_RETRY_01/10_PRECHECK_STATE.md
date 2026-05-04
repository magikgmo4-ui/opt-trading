---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01_PRECHECK
doc_type: precheck_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_PRECHECK_STATE — Etat avant retry

## Services critiques

| Service | Statut |
| --- | --- |
| tv-webhook | active |
| tv-perf | active |
| vision_bot | active |
| bot_vision_step2 | active |
| ngrok-tv | active |

## Inbox vision/SFTP

**CLEAN** — 0 fichier 0-byte, 0 .uploading

## macro-xau.timer

**DISABLED + INACTIVE**

## Quarantaine precedente

`/srv/sftp/shared_files/shared/quarantine/GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01_20260504T190858Z/`

- Contient 14 fichiers (9 x 0-byte PNG + 5 x .uploading)

## desk_bridge avant retry

- Service: failed (result: exit-code, status=2)
- Derniere erreur (avant quarantine): PIL.UnidentifiedImageError sur fichier 0-byte
