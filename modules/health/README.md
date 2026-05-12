# health

Unified observability module for automation surface health checks.

## Commands

```bash
bash modules/health/scripts/health-check              # text output
bash modules/health/scripts/health-check --json       # JSON machine-readable
bash modules/health/scripts/health-check perf         # filter surfaces
bash modules/health/scripts/health-alert              # alerting (Phase 2)
bash modules/health/scripts/health-dashboard          # dashboard (Phase 3)
bash modules/health/scripts/health-dashboard --json   # JSON export
bash modules/health/scripts/health-dashboard --html   # HTML static
```

## Status

```text
healthy  = surface is responding correctly
degraded = surface responds but with issues
down     = surface is not reachable
unknown  = could not determine status
```

## Phase 1 scope

- health check contract JSON
- registry of 10 automation surfaces
- cmd-health CLI with text and JSON output

## Phase 2 scope

- health-alert: stateful alerting for down surfaces
- Telegram notifications via TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID
- dedup: max 1 alert per surface per 30 min
- recovery notifications
- state stored in `_work/health/`

## Phase 2 env vars

```text
TELEGRAM_BOT_TOKEN  → Telegram bot token
TELEGRAM_CHAT_ID    → target chat ID
HEALTH_DOWN_THRESHOLD  → seconds before alert (default 300 = 5 min)
HEALTH_ALERT_COOLDOWN  → seconds between repeat alerts (default 1800 = 30 min)
```

## Phase 3 scope

- health-dashboard: read-only aggregation of health state
- text matrix with icons, staleness, last_seen
- JSON export for machine consumption
- HTML static page (dark theme)
- no server, no runtime mutation


## Status

```text
healthy  = surface is responding correctly
degraded = surface responds but with issues
down     = surface is not reachable
unknown  = could not determine status
```

## Phase 1 scope

- health check contract JSON
- registry of 10 automation surfaces
- cmd-health CLI with text and JSON output
- no alerting, no dashboard runtime, no circuit breakers
