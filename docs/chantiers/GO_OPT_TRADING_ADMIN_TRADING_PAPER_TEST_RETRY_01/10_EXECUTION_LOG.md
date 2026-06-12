# 10_EXECUTION_LOG

## Pre-check

| Check | Result |
|-------|--------|
| admin-trading SSH | PASS |
| Git state | `sot/mainline @ 260f0442` |
| tv-webhook.service | active (running) |
| Guards before | `ok: true` (all PASS) |

## Payload

```json
{
    "engine": "PAPER_TEST",
    "signal": "BUY",
    "symbol": "BTC/USDT",
    "tf": "1h",
    "price": 65000.0,
    "tp": 66000.0,
    "sl": 64000.0,
    "reason": "GO_PAPER_TEST_RETRY_01"
}
```

## Execution

```bash
curl -sS -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -d '{"engine":"PAPER_TEST","signal":"BUY","symbol":"BTC/USDT","tf":"1h","price":65000.0,"tp":66000.0,"sl":64000.0,"reason":"GO_PAPER_TEST_RETRY_01"}'
```

## Response

```json
{"ok": true}
```

## Service Logs

```
EXECUTION: {'ok': True, 'status': 'filled', 'execution_id': 'paper_BTC/USDT_123', 'filled_qty': 0.1, 'avg_price': 65000.0, 'adapter': 'paper'}
POSITION UPDATED: {'ok': True, 'status': 'opened', 'position': {'symbol': 'BTC/USDT', 'side': 'BUY', 'qty': 0.1, 'entry_price': 65000.0, 'opened_at': '2026-05-14T02:48:18.649769+00:00', 'pnl': 0.0, 'status': 'OPEN'}}
POST /tv HTTP/1.1" 200 OK
```

## Events Log

```json
{"key": null, "engine": "PAPER_TEST", "signal": "BUY", "symbol": "BTC/USDT", "tf": "1h", "price": 65000.0, "tp": 66000.0, "sl": 64000.0, "reason": "GO_PAPER_TEST_RETRY_01", "_ts": "2026-05-14T02:48:17.765972+00:00", "_ip": "127.0.0.1", "qty": 0.1, "risk_usd": 100.0, "risk_real_usd": 100.0}
```

## Position State

```json
{
    "BTC/USDT": {
        "symbol": "BTC/USDT",
        "side": "BUY",
        "qty": 0.1,
        "entry_price": 65000.0,
        "opened_at": "2026-05-14T02:48:18.649769+00:00",
        "pnl": 0.0,
        "status": "OPEN"
    }
}
```

## Guards After

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

## Analysis

- PAPER_TEST accepted by guards (ok: true before)
- Executed through paper adapter (no real trade)
- Position tracked in positions.json
- Events logged in events.jsonl
- Guards still ok: true after execution
- active_engine remains null (PAPER_TEST not aggressive)

## RISKS

- À qualifier.
