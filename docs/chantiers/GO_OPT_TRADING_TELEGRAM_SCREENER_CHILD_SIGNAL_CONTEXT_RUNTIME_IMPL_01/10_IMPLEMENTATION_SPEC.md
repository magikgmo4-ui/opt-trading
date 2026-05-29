# Implementation Spec

## Change
Create a minimal runtime module `modules/telegram_screener/` with:
- a latest-only Data Center reader
- standard module scripts (`cmd.sh`, `menu.sh`, `sanity_check.sh`, `install_shortcuts.sh`)

## Behavior
- read path: `data/data_center/views/market_metrics/latest.json`
- fallback: `silent_empty` -> `None`
- return a lightweight screener context structure plus raw payload
