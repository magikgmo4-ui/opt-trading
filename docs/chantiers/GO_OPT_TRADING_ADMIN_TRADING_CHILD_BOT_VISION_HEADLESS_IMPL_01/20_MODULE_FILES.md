---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01_FILES
doc_type: module_files
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_MODULE_FILES

## Fichiers crees

### modules/bot_vision/headless_capture/

| Fichier | Taille | Role |
| --- | --- | --- |
| package.json | 492 B | npm config, dependance playwright |
| capture_headless.js | 5954 B | Script principal de capture |
| profiles.example.json | 164 B | Profil(s) de capture (URLs) |
| README.md | 1616 B | Documentation utilisateur |

## Usage

```bash
cd /opt/trading/modules/bot_vision/headless_capture

# Capture unique
node capture_headless.js --profile profiles.example.json --once

# Verifier dependances
npm run check
```

## Contrat de sortie

| Aspect | Implementation |
| --- | --- |
| PNG | screen_{source}_{symbol}_{tf}_{ts}.png |
| JSON sidecar | screen_{source}_{symbol}_{tf}_{ts}.json |
| Ecriture atomique | .uploading -> rename |
| Taille min | 1 KB (sinon discard) |
| 0-byte garde | Verifie avant rename, discard si 0 |
| Cleanup stale | .uploading > 5 min supprimes |
| Dossier sortie | /srv/sftp/shared_files/shared/vision_inbox |
| Temp | /tmp/bot_vision_headless |

## Sidecar JSON schema

```json
{
  "producer": "bot_vision_headless",
  "capture_mode": "playwright_chromium",
  "source": "tradingview",
  "symbol": "BTCUSDT.P",
  "timeframe": "H1",
  "url": "...",
  "viewport": {"width": 1920, "height": 1080},
  "created_at_utc": "2026-05-04T21:00:41Z",
  "output_png": "screen_...",
  "output_json": "screen_...",
  "status": "ready"
}
```

## RISKS

- À qualifier.
