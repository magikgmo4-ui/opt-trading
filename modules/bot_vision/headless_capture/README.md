# bot_vision_headless — headless_capture

Headless browser capture for bot_vision pipeline.  
Uses Playwright + Chromium to capture trading chart dashboards
and writes them directly to vision_inbox with atomic writes.

## Dependencies

- Node.js >= 18
- Playwright + Chromium

## Install

```bash
cd modules/bot_vision/headless_capture
npm install
npx playwright install chromium
```

## Usage

```bash
# Single capture cycle (all profiles)
node capture_headless.js --profile profiles.example.json --once

# Check dependencies
npm run check

# Run example profile
npm run capture:example
```

## Profiles

Edit `profiles.example.json` to add URLs for capture.
Each profile needs: `source`, `url`. Optional: `symbol`, `timeframe`.

## Output

Files are written atomically to vision_inbox:

```
vision_inbox/
  screen_{source}_{symbol}_{timeframe}_{timestamp}.png
  screen_{source}_{symbol}_{timeframe}_{timestamp}.json
```

Atomic write: `.uploading` temporary file → rename to final name.
Stale `.uploading` files (> 5 min) are cleaned up automatically.

## Env vars

| Var | Default | Description |
| --- | --- | --- |
| BOT_VISION_TMP | /tmp/bot_vision_headless | Temp directory |
| BOT_VISION_OUT | /srv/sftp/shared_files/shared/vision_inbox | Output directory |

## Contract

- Never writes 0-byte files
- Files < 1 KB are discarded
- `.uploading` suffix during write, atomically renamed
- Sidecar JSON produced alongside every PNG
- Compatible with vision_bot watch loop
- Compatible with desk_bridge crop pipeline
- ShareX remains fallback
