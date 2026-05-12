# 30_PAPER_TEST_CONFIG

Le mode `PAPER_TEST` utilise la même architecture que `LIVE` mais avec les paramètres suivants :

- `RUNNER_MODE=PAPER`
- `LEDGER_PATH=/data/ledger_paper.json`
- `BROKER_API_URL=https://sandbox.broker.com`
- `TRADE_ALLOWED=false` (Hardcoded protection)
