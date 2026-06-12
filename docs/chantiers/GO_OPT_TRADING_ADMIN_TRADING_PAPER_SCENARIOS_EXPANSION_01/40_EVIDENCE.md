# 40_EVIDENCE

## Scenario A Evidence

Service logs:
```
EXECUTION: {'ok': True, 'status': 'filled', 'execution_id': 'paper_ETH/USDT_123', 'filled_qty': 1.0, 'avg_price': 3500.0, 'adapter': 'paper'}
POSITION UPDATED: {'ok': True, 'status': 'opened', 'position': {'symbol': 'ETH/USDT', 'side': 'SELL', 'qty': 1.0, 'entry_price': 3500.0, ...}}
```

## Scenario B Evidence

HTTP 400 responses with descriptive error messages. No execution logs. No position changes.

## Scenario C Evidence

Guards response:
```json
{
    "ok": false,
    "guards": {
        "active_engine": {"ok": false, "value": "COINM_SHORT", "expected": "unset or non-aggressive engine"}
    }
}
```

HTTP 409 response. No execution logs. No position changes.

## Scenario D Evidence

```bash
ls -la /opt/trading/state/ledger*
# Only ledger_paper.json exists

cat /opt/trading/state/ledger_paper.json
# {}
```

No ledger_live file. No live data contamination.

## RISKS

- À qualifier.
