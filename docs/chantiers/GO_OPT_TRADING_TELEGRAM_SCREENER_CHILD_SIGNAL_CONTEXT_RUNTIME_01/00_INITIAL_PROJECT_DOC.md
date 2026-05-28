# GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_CONTEXT_RUNTIME_01

## Goal
Implement the runtime consumer for `telegram_screener__signal_context` so Telegram Screener can read canonical `market_metrics.v1` context from the Data Center view.

## Context
After Data Center Phase 2C, the remaining `market_metrics.v1` runtime consumer still marked `not_started` is:
- `telegram_screener__signal_context`

The consumer registry already defines its canonical contract:
- contract class: `market_metrics.v1`
- read path: `data/data_center/views/market_metrics/latest.json`
- access pattern: `latest_only`
- fallback: `silent_empty`

## Scope
- Telegram Screener runtime consumer implementation
- consumer registry status update
- focused tests proving runtime read behavior
- this chantier documentation and bundle metadata
