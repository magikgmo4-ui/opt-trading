---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01_ARTIFACT_FLOW
doc_type: artifact_flow_map
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 20_ARTIFACT_FLOW_MAP - Artifact Flow Map

## Flux complet

```
┌─────────────────────────────────────────────────────────────────────┐
│ PRODUCER: Bot Vision Headless (Playwright/Chromium)                 │
│ Script: modules/bot_vision/headless_capture/capture_headless.js    │
│ Timer: bot-vision-headless-capture.timer (10min)                   │
│ Wrapper: scripts/run_bot_vision_headless_capture.sh                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
            vision_inbox/ (SFTP shared)
            screen_{source}_{symbol}_{tf}_{ts}.png
            screen_{source}_{symbol}_{tf}_{ts}.json  (sidecar)
            Atomic write: .uploading → rename
            Guard: < 1KB discarded, 0-byte discarded
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│ CONSUMER: vision_bot (watch loop)                                   │
│ Module: modules/vision_bot/app/vision_bot.py                       │
│ Service: vision_bot.service (long-running)                         │
│ Role: OCR + move to vision_processed/                              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
            vision_processed/
            screen_*.png (moved from vision_inbox)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ADAPTER: desk_bridge (timer-driven oneshot)                        │
│ Script: scripts/desk_bridge/bridge_vision_to_desk_inbox.sh         │
│ Timer: desk_bridge.timer (10min)                                   │
│ Input: newest screen_*.png from vision_processed or vision_inbox   │
│ Process: crop 2x2 → 4 quadrants (BTC, XAU, SOL, ETH)              │
│ Guard: anti .uploading, anti 0-byte                                │
│ Output: {SYMBOL}_{TF}_{ts}.png → inbox/                            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
            inbox/ (SFTP shared)
            {SYMBOL}_H1_{ts}.png  (4 files per cycle)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│ INGEST: desk_snapshot_ingest                                       │
│ Module: modules/desk_snapshot_ingest/ingest_snapshots.py           │
│ Called by: desk_bridge via cmd-desk_snapshot_ingest ingest_once    │
│ Process: move inbox → desk/snapshots/{SYMBOL}/                     │
│ Output: desk/snapshots/latest.json + history.jsonl                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
            desk/snapshots/{SYMBOL}/{SYMBOL}_H1_{ts}.png
            desk/snapshots/latest.json
            desk/snapshots/history.jsonl
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│ FUTURE CONSUMER: Desk Pro                                          │
│ Module: modules/desk_pro_runner/                                   │
│ Input: desk/snapshots/latest.json + PNG files                      │
│ Last known run: 2026-04-05                                         │
└─────────────────────────────────────────────────────────────────────┘
```

## Détail par étape

### 1. capture_headless.js (Producer)

| Champ | Valeur |
| --- | --- |
| Producer | `bot_vision_headless` |
| Artifact | `screen_{source}_{symbol}_{tf}_{ts}.png` + `.json` sidecar |
| Format PNG | 1920×1080 screenshot |
| Format JSON | `{producer, capture_mode, source, symbol, timeframe, url, viewport, created_at_utc, output_png, output_json, status}` |
| Destination | `/srv/sftp/shared_files/shared/vision_inbox/` |
| Atomic write | `.uploading` suffix → rename |
| Garde | < 1KB discarded, 0-byte discarded, stale `.uploading` > 5min cleaned |
| Cadence | 10 min (timer) |
| Statut actuel | **FAILED** — playwright non installé |

### 2. vision_bot (OCR Watch)

| Champ | Valeur |
| --- | --- |
| Consumer | `vision_bot` |
| Input | `vision_inbox/screen_*.png` |
| Output | move → `vision_processed/` |
| Role | OCR, metadata extraction |
| Statut | **CONFIRMED** — active (running) |

### 3. desk_bridge (Adapter)

| Champ | Valeur |
| --- | --- |
| Adapter | `desk_bridge` |
| Input | newest `screen_*.png` from `vision_processed` or `vision_inbox` |
| Process | crop 2x2 → 4 quadrants |
| Mapping | `MAP0=BTCUSDT.P, MAP1=XAUUSD, MAP2=SOLUSDT.P, MAP3=ETHUSDT.P` |
| Output | `inbox/{SYMBOL}_H1_{ts}.png` (4 files) |
| Garde | anti `.uploading`, anti 0-byte |
| Statut | **CONFIRMED** — last run SUCCESS |

### 4. desk_snapshot_ingest (Ingest)

| Champ | Valeur |
| --- | --- |
| Module | `desk_snapshot_ingest` |
| Input | `inbox/{SYMBOL}_H1_{ts}.png` |
| Output | `desk/snapshots/{SYMBOL}/{SYMBOL}_H1_{ts}.png` + `latest.json` + `history.jsonl` |
| Called by | desk_bridge (`cmd-desk_snapshot_ingest ingest_once`) |
| Statut | **CONFIRMED** — active |

### 5. Desk Pro (Future Consumer)

| Champ | Valeur |
| --- | --- |
| Consumer | `desk_pro_runner` |
| Input attendu | `desk/snapshots/latest.json` + PNG files |
| Dernier run | 2026-04-05 |
| Statut | **HYPOTHESIS** — consumer non actif, input contract non formalisé |

## Matrice de statut

| Step | Producer | Artifact | Consumer | Statut |
| --- | --- | --- | --- | --- |
| 1 | capture_headless.js | PNG + JSON sidecar | vision_bot | **STALE** (playwright missing) |
| 2 | vision_bot | screen_*.png moved | desk_bridge | **CONFIRMED** |
| 3 | desk_bridge | 4× cropped PNG | desk_snapshot_ingest | **CONFIRMED** |
| 4 | desk_snapshot_ingest | latest.json + PNG | Desk Pro | **CONFIRMED** (output) |
| 5 | Desk Pro | synthesis/report | operator | **HYPOTHESIS** (not running) |

## Source alternative: ShareX

Le flux ShareX (cursor-ai → SFTP → vision_inbox) reste le fallback fonctionnel quand headless capture échoue. Les fichiers `screen_*.png` dans `vision_inbox` et `vision_processed` proviennent actuellement de cette source.

## RISKS

- À qualifier.
