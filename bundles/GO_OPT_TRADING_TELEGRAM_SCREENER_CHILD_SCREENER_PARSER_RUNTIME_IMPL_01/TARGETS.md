# Targets

- implement `modules/telegram_screener/parser/` runtime (trade, news, alpha)
- normalize raw Telegram messages into `ScreenerSignal` canonical format
- provide representative fixture samples for all three signal types
- prove parser behavior with focused tests (no network, no live API)
- update module sanity check to validate parser surface
