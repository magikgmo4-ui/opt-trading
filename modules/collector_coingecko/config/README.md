# collector_coingecko config

Committed file:
- `defaults.toml`

Optional uncommitted local files:
- `local.toml`
- `secrets.local.env`

Deterministic resolution order:
1. `defaults.toml`
2. `local.toml`
3. environment variables

Required secret env var:
- `COLLECTOR_COINGECKO__API__KEY`

Useful optional overrides:
- `COLLECTOR_COINGECKO__API__BASE_URL`
- `COLLECTOR_COINGECKO__COLLECTION__COIN_IDS`
- `COLLECTOR_COINGECKO__COLLECTION__VS_CURRENCY`

For list overrides, use a comma-separated string such as:
- `COLLECTOR_COINGECKO__COLLECTION__COIN_IDS=bitcoin,ethereum`

Do not store secrets in TOML files.
