# CDP Signal Event Bridge — Runtime Integration

## Objective

Wire TradingView CDP alerts into the Data Center signal_event.v1 pipeline.

## Changes

### 1. `/tv/cdp` endpoint — `webhook_server.py`

New endpoint separate from trading `/tv`. Monitor-only, no broker, no orders.

Flow:
```
TradingView webhook → POST /tv/cdp → cdp_normalizer → validate → write_signal_event → DC views
```

### 2. `signal_event_writer.py` — `modules/data_center/`

Writes normalized signal events to:
- `data/data_center/views/signal_event.v1/latest.json` (rolling 50)
- `data/data_center/views/signal_event.v1/by_symbol/<SYMBOL>/latest.json` (per-symbol)
- Updates runtime registry via `update_producer_last_write()`

### Test

```bash
# Simulate SPCX vwap_reclaim alert
curl -X POST http://localhost:8000/tv/cdp \
  -H "Content-Type: application/json" \
  -d '{"ticker":"SPCX","interval":"5","event":"vwap_reclaim","close":171.5,"volume":1250000}'

# Expected: {"ok":true,"mode":"monitor_only","event":"vwap_reclaim","symbol":"SPCX"}
```

### Guards
- Forbidden fields in raw payload are NOT copied to normalized output
- `risk_mode` must be `monitor_only`
- No broker, no order, no execution, no position management

## Files

| File | Role |
|---|---|
| `webhook_server.py` | +`/tv/cdp` endpoint |
| `modules/data_center/signal_event_writer.py` | DC sink for signal events |
| `modules/tradingview/cdp_normalizer.py` | Already exists (PR #1191) |

## Deployment

```bash
cd /opt/trading && git pull && sudo systemctl restart tv-webhook.service
```
