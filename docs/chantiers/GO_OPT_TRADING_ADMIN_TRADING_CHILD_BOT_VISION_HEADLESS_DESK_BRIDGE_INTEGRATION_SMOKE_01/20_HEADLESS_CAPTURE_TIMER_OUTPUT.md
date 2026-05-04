---
doc_id: INTEGRATION_SMOKE_01_CAPTURE
doc_type: headless_capture_output
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_HEADLESS_CAPTURE_TIMER_OUTPUT

## Timer operationnel depuis 2h+

| Timestamp | PNG Size | Status |
| --- | --- | --- |
| 17:59 | 94 KB | processed by vision_bot |
| 18:10 | 60 KB | processed |
| 18:20 | 107 KB | processed |
| 18:30 | 87 KB | processed |
| 18:40 | 86 KB | processed |
| 18:51 | 133 KB | processed |
| 19:01 | 93 KB | processed |
| 19:11 | 134 KB | processed |
| 19:21 | 106 KB | processed |
| 19:31 | 75 KB | processed |
| 19:42 | ~90 KB | processed (last) |

**10+ cycles automatiques**, tous SUCCESS.

## Verifications

| Check | Resultat |
| --- | --- |
| PNG valides (> 1 KB) | OUI (60-134 KB) |
| JSON sidecar | OUI (497 B each) |
| 0-byte | 0 |
| .uploading restant | 0 |
| Atomic write | OUI (confirme par timer logs) |
| Timer stable | OUI (2h+ sans interruption) |
