# collector_binance_spot config

Committed file:
- `defaults.toml`

Optional uncommitted local files:
- `local.toml`

Deterministic resolution order:
1. `defaults.toml`
2. `local.toml`
3. environment variables

Useful optional overrides:
- `COLLECTOR_BINANCE_SPOT__API__BASE_URL`
- `COLLECTOR_BINANCE_SPOT__COLLECTION__SYMBOLS`
- `COLLECTOR_BINANCE_SPOT__COLLECTION__TICKER_TYPE`

For list overrides, use a comma-separated string such as:
- `COLLECTOR_BINANCE_SPOT__COLLECTION__SYMBOLS=BTCUSDT,ETHUSDT`

No secret is required for the default public market-data path.
