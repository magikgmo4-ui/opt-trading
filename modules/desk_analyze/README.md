# desk_analyze — Step B (single /analyze output)
Reads `/opt/trading/desk/snapshots/latest.json` (produced by desk_snapshot_ingest)
and builds ONE consolidated desk report (BTC/XAU/SOL/ETH by default).

This is the key fix: /analyze must NOT depend on "reading the last photo from Telegram".
It reads local latest.json (source of truth).

## Defaults
- INDEX_FILE: /opt/trading/desk/snapshots/latest.json
- DESK_SYMBOLS: BTCUSDT.P,XAUUSD,SOLUSDT.P,ETHUSDT.P
- STALE_MINUTES: 15
- TIMEZONE: America/Montreal

## Commands
- preview: prints the consolidated report
- preview_json: prints JSON structure
- send: sends to Telegram using TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID

## Env needed for send
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

Optional:
- TELEGRAM_API_BASE (defaults to https://api.telegram.org)

## Quick
modules/desk_analyze/scripts/sanity_check.sh
modules/desk_analyze/scripts/cmd.sh preview
