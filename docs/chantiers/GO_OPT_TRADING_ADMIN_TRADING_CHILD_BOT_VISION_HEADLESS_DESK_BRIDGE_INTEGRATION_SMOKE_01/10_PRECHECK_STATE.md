---
doc_id: INTEGRATION_SMOKE_01_PRECHECK
doc_type: precheck_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_PRECHECK_STATE

## Services

| Service | Statut |
| --- | --- |
| tv-webhook | active |
| tv-perf | active |
| vision_bot | active |
| bot_vision_step2 | active |
| ngrok-tv | active |
| bot-vision-headless-capture.timer | active (since 17:28, 2h+) |
| macro-xau.timer | disabled + inactive |

## Timer state

- Next trigger: ~7 min
- Last run: exit 0/SUCCESS
- 10+ cycles completed automatically

## Inbox state

- 0 corrupted files (0-byte or .uploading)
- vision_inbox: JSON sidecars only (PNGs already processed by vision_bot)
- vision_processed: latest PNG captures (60-133 KB)
- vision_outbox: OCR .md + .txt outputs

## desk_bridge

- Last run: 19:41, exit 0/SUCCESS
- Processed headless capture → 4 quadrants → desk/snapshots/
- No PIL crash
