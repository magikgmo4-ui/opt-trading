---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01_PRECHECK
doc_type: precheck_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_PRECHECK_STATE — Etat avant reparation

## Services critiques (avant)

| Service | Statut |
| --- | --- |
| tv-webhook | active |
| tv-perf | active |
| vision_bot | active |
| bot_vision_step2 | active |
| ngrok-tv | active |

## macro-xau (avant)

| Unite | Statut |
| --- | --- |
| macro-xau.timer | enabled + active |
| macro-xau.service | failed (exit-code 203/EXEC) |
| macro-xau.timer trigger | every 30min, next in ~55min |

## Fichiers corrompus dans vision_inbox (avant)

### 0-byte PNGs (echecs SFTP mars 2026)

9 fichiers:
- screen_2026-03-05_23-08-47_8.png (0 B)
- screen_2026-03-05_23-45-30_2.png (0 B)
- screen_2026-03-05_23-55-30_0.png (0 B)
- screen_2026-03-06_01-37-07_3.png (0 B)
- screen_2026-03-06_01-57-07_9.png (0 B)
- screen_2026-03-06_02-07-07_3.png (0 B)
- screen_2026-03-06_03-37-07_9.png (0 B)
- screen_2026-03-06_03-57-07_0.png (0 B)
- screen_2026-03-06_04-07-07_7.png (0 B)

### .uploading partiels (SFTP interrompus avril 2026)

5 fichiers:
- screen_2026-04-03_10-56-15_7.png.uploading.* (535 KB)
- screen_2026-04-03_16-16-14_5.png.uploading.* (515 KB)
- screen_2026-04-04_07-36-16_2.png.uploading.* (339 KB)
- screen_2026-04-04_07-46-16_5.png.uploading.* (338 KB)
- screen_2026-04-04_09-36-16_5.png.uploading.* (338 KB)

### Total a quarantainer: 14 fichiers
