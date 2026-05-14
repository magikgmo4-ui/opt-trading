# 50_ROLLBACK

## What Changed

- `/opt/trading/state/positions.json` — removed `BTC/USDT` entry

## Rollback Steps

To restore the position:

```python
import json
with open("/opt/trading/state/positions.json") as f:
    d = json.load(f)
d["BTC/USDT"] = {
    "symbol": "BTC/USDT",
    "side": "BUY",
    "qty": 0.1,
    "entry_price": 65000.0,
    "opened_at": "2026-05-14T02:48:18.649769+00:00",
    "pnl": 0.0,
    "status": "OPEN"
}
with open("/opt/trading/state/positions.json", "w") as f:
    json.dump(d, f, indent=2)
```

## Risk

Minimal. Paper position only, no real money affected.
