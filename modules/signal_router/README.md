# signal_router

Reçoit les webhooks TradingView, valide et normalise vers un signal JSON canonique.

## Flux

```
POST /webhook (TradingView JSON) → validate → normalize → NormalizedSignal JSON
```

## Canonical signal JSON

```json
{
  "signal_id": "uuid",
  "ticker": "BTCUSDT",
  "side": "BUY",
  "price": 65000.0,
  "timestamp": 1778917789.5,
  "strategy_id": "breakout_v2",
  "tf": "1h",
  "tp": 67000.0,
  "sl": 63000.0,
  "reason": "breakout",
  "source": "tradingview"
}
```

## Commandes

```bash
scripts/cmd.sh start    # démarre sur 127.0.0.1:18900
scripts/cmd.sh stop
scripts/cmd.sh health   # GET /health
scripts/cmd.sh smoke    # POST test signal → signal JSON
scripts/cmd.sh sanity   # structure + tests
scripts/cmd.sh test     # unit tests (12 tests)
```

## Config

```bash
SIGNAL_ROUTER_PORT=18900   # default
SIGNAL_ROUTER_HOST=127.0.0.1
```

## État

```
Tests    12/12 PASS
Sanity   PASS
Smoke    PASS — signal BTCUSDT BUY routed
```
