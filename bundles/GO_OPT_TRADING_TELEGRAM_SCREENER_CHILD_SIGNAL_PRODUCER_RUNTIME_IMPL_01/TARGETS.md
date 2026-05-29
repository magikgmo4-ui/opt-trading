# Targets

- implement `modules/telegram_screener/signal/` runtime (producer + adapter)
- produce normalized `ScreenerProducedSignal` from parsed parser signals
- adapt signals to `telegram_claim.v1` format for Desk Pro consumption
- prove with 18 focused tests (no network, no live API)
