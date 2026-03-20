# collector_binance_spot

Second real pilot collector module for Binance Spot public market data.

Status:
- provider implemented at minimal V1 pilot scope
- provider validated live and lightly hardened
- execution mode: oneshot only
- no auth required for the public market-data path
- no daemon or scheduler

Implemented target:
- provider: Binance Spot Market Data API
- module_id: `collector_binance_spot`
- provider_id: `binance_spot`
- sanity target: `/api/v3/ping`
- metadata discovery target: `/api/v3/exchangeInfo`
- first collection target: `/api/v3/ticker/24hr`
- default allowlist: `BTCUSDT`, `ETHUSDT`

Run entrypoints:
- `scripts/sanity_check.sh`
- `scripts/collector_binance_spot_cmd.sh run`
- `scripts/collector_binance_spot_menu.sh`

Config:
- committed defaults: `config/defaults.toml`
- optional local overrides: `config/local.toml` (uncommitted)
- no secret is required for the default public market-data path

Outputs:
- raw captures: `outputs/raw/<run_id>/exchange_info.json`, `outputs/raw/<run_id>/ticker_24hr.json`
- normalized output: `outputs/normalized/pair_market_snapshot_<run_id>.json`
- canonical artifacts: `manifest.json`, `status.json`, `latest.json`, `events.jsonl`, `errors.jsonl`

See `docs/01_runbook.txt` for exact local run steps.
