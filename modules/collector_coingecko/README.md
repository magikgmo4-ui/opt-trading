# collector_coingecko

First real pilot collector module for CoinGecko API.

Status:
- provider implemented at minimal V1 pilot scope
- pilot hardening pass applied
- execution mode: oneshot only
- no daemon or scheduler

Implemented target:
- provider: CoinGecko API
- module_id: `collector_coingecko`
- provider_id: `coingecko`
- first execution mode: oneshot
- sanity target: `/ping`
- first collection target: `/coins/markets`
- default allowlist: `bitcoin`, `ethereum`
- default `vs_currency`: `usd`

Run entrypoints:
- `scripts/sanity_check.sh`
- `scripts/collector_coingecko_cmd.sh run`
- `scripts/collector_coingecko_menu.sh`

Config:
- committed defaults: `config/defaults.toml`
- optional local overrides: `config/local.toml` (uncommitted)
- secret env var: `COLLECTOR_COINGECKO__API__KEY`

Outputs:
- raw capture: `outputs/raw/<run_id>/coins_markets.json`
- normalized output: `outputs/normalized/market_snapshot_<run_id>.json`
- canonical artifacts: `manifest.json`, `status.json`, `latest.json`, `events.jsonl`, `errors.jsonl`

See `docs/01_runbook.txt` for exact local run steps.
