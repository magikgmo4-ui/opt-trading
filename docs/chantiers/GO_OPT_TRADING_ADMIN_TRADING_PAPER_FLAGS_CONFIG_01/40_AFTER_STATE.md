# 40_AFTER_STATE

## Guards (AFTER)

```json
{
    "ok": true,
    "mode": "PAPER_TEST",
    "guards": {
        "runner_mode": {"ok": true, "value": "PAPER", "expected": "PAPER"},
        "simulation_mode": {"ok": true, "value": "true", "expected": "true"},
        "trade_allowed": {"ok": true, "value": "false", "expected": "false"},
        "ledger_path": {"ok": true, "value": "/opt/trading/state/ledger_paper.json", "expected": "path ending in ledger_paper.json"},
        "active_engine": {"ok": true, "value": "unset", "expected": "unset or non-aggressive engine"},
        "paper_adapter": {"ok": true, "value": "registered", "expected": "registered"}
    },
    "reasons": []
}
```

## Service

| Field | Value |
|-------|-------|
| Service | `tv-webhook.service` |
| Status | active (running) |
| PID | 828006 |
| Port | 8000 |

## Env File

Paper flags present in `/opt/trading/.env`:
- `RUNNER_MODE=PAPER`
- `SIMULATION_MODE=true`
- `TRADE_ALLOWED=false`
- `LEDGER_PATH=/opt/trading/state/ledger_paper.json`

## Router State

`/opt/trading/state/router_state.json`: `{"active_engine": null, "updated_at": "2026-05-14T05:50:00+00:00"}`

## Ledger

`/opt/trading/state/ledger_paper.json`: `{}` (empty, exists)
