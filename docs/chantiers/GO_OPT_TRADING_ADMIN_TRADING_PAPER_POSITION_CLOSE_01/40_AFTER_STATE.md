# 40_AFTER_STATE

## Guards

```json
{
    "ok": true,
    "mode": "PAPER_TEST",
    "guards": {
        "runner_mode": {"ok": true, "value": "PAPER"},
        "simulation_mode": {"ok": true, "value": "true"},
        "trade_allowed": {"ok": true, "value": "false"},
        "ledger_path": {"ok": true, "value": "/opt/trading/state/ledger_paper.json"},
        "active_engine": {"ok": true, "value": "unset"},
        "paper_adapter": {"ok": true, "value": "registered"}
    }
}
```

## Positions (AFTER)

| Symbol | Side | Qty | Entry | Status | Source |
|--------|------|-----|-------|--------|--------|
| BTCUSDT | BUY | 0.1 | 50000.0 | OPEN | pre-existing |
| PERFTEST1 | BUY | 10.0 | 50000.0 | OPEN | pre-existing |
| PERFTEST2 | SELL | 10.0 | 49500.0 | OPEN | pre-existing |

Target position BTC/USDT removed. Pre-existing positions unchanged.
