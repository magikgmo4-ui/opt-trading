# collector_telegram

Read-only Telegram batch collector for building a real message corpus before any channel scoring.

Scope:
- fetch recent messages from selected Telegram channels
- persist raw message corpus locally under ignored runtime outputs
- apply lightweight parsing with existing repo parsers when possible
- publish batch status and per-channel results for operator review

Non-scope:
- no write-back to Telegram
- no DeskPro claim production
- no channel scoring or ranking yet

Entry points:
- `scripts/run_telegram_collector.sh`
- `modules/collector_telegram/scripts/cmd.sh`

Default runtime artifacts stay local and ignored:
- `modules/collector_telegram/outputs/`
- `modules/collector_telegram/logs/`
- `modules/collector_telegram/runtime/`
