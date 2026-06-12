---
doc_id: HEADLESS_CLOSEOUT_01_ARCH
doc_type: final_architecture
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_FINAL_ARCHITECTURE — Bot Vision Pipeline

## Pipeline automatique

```
bot-vision-headless-capture.timer (10 min, 30s jitter)
  |
  v
capture_headless.js (Playwright/Chromium)
  |-- page.goto(TradingView URL)
  |-- page.screenshot() -> PNG
  |-- atomic write: .uploading -> screen_*.png
  |-- sidecar JSON
  v
/srv/sftp/shared_files/shared/vision_inbox/
  |
  v
vision_bot (watch loop, OCR)
  |-- detecte screen_*.png
  |-- OCR (tesseract ou dummy)
  |-- deplace vers vision_processed/
  |-- ecrit .md + .txt dans vision_outbox/
  v
desk_bridge.timer (10 min)
  |-- pick_latest() skip .uploading + 0-byte
  |-- crop_with_python() PIL.Image.open() + guard
  |-- 4 quadrants -> /shared/inbox/
  |-- desk_snapshot_ingest -> desk/snapshots/
  v
Desk Pro (PAPER)
  |-- 11 modules: market_scanner -> portfolio_engine
  v
/shared/desk_pro/latest/ (consomme par db-layer/student)
```

## Fichiers cles

| Fichier | Role |
| --- | --- |
| modules/bot_vision/headless_capture/capture_headless.js | Capture headless |
| modules/bot_vision/headless_capture/profiles.example.json | URLs de capture |
| modules/bot_vision/headless_capture/package.json | npm config |
| scripts/run_bot_vision_headless_capture.sh | Wrapper shell |
| scripts/desk_bridge/bridge_vision_to_desk_inbox.sh | Bridge crop + ingest |
| modules/bot_vision/headless_capture/systemd/*.service | Service oneshot |
| modules/bot_vision/headless_capture/systemd/*.timer | Timer 10 min |

## Dossiers runtime

| Dossier | Contenu |
| --- | --- |
| vision_inbox/ | Nouveaux PNG + JSON (temporaire) |
| vision_processed/ | PNGs traites par OCR |
| vision_outbox/ | .md + .txt (OCR output) |
| /shared/inbox/ | Quadrants crops (temporaire) |
| desk/snapshots/ | Snapshots archives par symbole |
| /shared/desk_pro/latest/ | Outputs Desk Pro |

## RISKS

- À qualifier.
