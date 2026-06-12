---
doc_id: BRIDGE_GUARD_01_POSTCHECK
doc_type: postcheck
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_RUNTIME_POSTCHECK

## Services

| Service | Statut |
| --- | --- |
| tv-webhook | active |
| tv-perf | active |
| vision_bot | active |
| bot_vision_step2 | active |
| ngrok-tv | active |
| bot-vision-headless-capture.timer | active |
| desk_bridge.timer | active |
| macro-xau.timer | disabled + inactive |

## Corrupted files

0 (zero) — 0-byte et .uploading absents de vision_inbox et vision_processed.

## desk_bridge

- Dernier run: exit 0, crop + ingest OK
- Timer actif, prochain cycle automatique
- Patch en place sur le script live

## RISKS

- À qualifier.
