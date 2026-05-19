# Airtable Bridge

Non-blocking module for sending records to Airtable tables from opt-trading.

## Structure

```
modules/airtable_bridge/
├── app/
│   ├── __init__.py
│   ├── client.py          # REST API client (POST, batch, retry, fail-open)
│   └── payloads.py        # Dataclass payloads (trade, signal, backtest, go_status)
├── scripts/
│   ├── sanity_check.sh    # Check env + API connectivity
│   ├── cmd.sh             # CLI command for single invocation
│   └── menu.sh            # Interactive menu
├── .env.example           # Template config
└── README.md              # This file
```

## Usage

### 1. Configure

```bash
cp .env.example .env
# Edit .env with your API key and base ID
export AIRTABLE_API_KEY=your_key
export AIRTABLE_BASE_ID=your_base_id
```

### 2. Sanity check

```bash
bash scripts/sanity_check.sh
```

### 3. Send data

```bash
# CLI
bash scripts/cmd.sh Trades ./my_trade.json

# Interactive menu
bash scripts/menu.sh

# Python API
python3 -c "
from app.client import send_signal
result = send_signal({'source': 'webhook', 'symbol': 'BTC/USD', 'signal': 'buy'})
print(result)
"
```

## Design

- **Fail-open**: errors are logged, never block the calling process
- **Batch**: max 10 records per request
- **Retry**: exponential backoff (3 attempts) on 429 rate limits
- **Timeout**: 10s per request
- **No secrets in code**: credentials via environment variables only

## Tables

| Table       | Payload         | Fields                                     |
|-------------|-----------------|--------------------------------------------|
| Trades      | TradePayload    | symbol, direction, entry_price, exit_price, quantity, pnl, status, notes, tags |
| Signals     | SignalPayload   | source, timestamp, symbol, signal, confidence, reviewed_by, notes |
| Backtests   | BacktestPayload | strategy, period, sharpe, drawdown, trades_count, verdict, notes |
| GO_Status   | GOStatusPayload | go_id, status, machine, branch, next_go, updated_at |

## Constraints

- Do not commit `.env` files
- Do not expose API keys in code or logs
- Do not block core opt-trading processes
