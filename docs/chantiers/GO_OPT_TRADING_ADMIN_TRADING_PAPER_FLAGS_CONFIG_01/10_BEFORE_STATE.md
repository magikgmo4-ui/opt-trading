# 10_BEFORE_STATE

## admin-trading Git

| Field | Value |
|-------|-------|
| HEAD | `6a48c1ee` |
| Branch | `sot/mainline` |

## Webhook Service

| Field | Value |
|-------|-------|
| Service | `tv-webhook.service` |
| Status | active (running) |
| PID | 827009 |
| Port | 8000 |

## Guards (BEFORE)

```json
{
    "ok": false,
    "mode": "PAPER_TEST",
    "guards": {
        "runner_mode": {"ok": false, "value": "unset", "expected": "PAPER"},
        "simulation_mode": {"ok": false, "value": "unset", "expected": "true"},
        "trade_allowed": {"ok": false, "value": "unset", "expected": "false"},
        "ledger_path": {"ok": false, "value": "unset", "expected": "path ending in ledger_paper.json"},
        "active_engine": {"ok": false, "value": "COINM_SHORT", "expected": "unset or non-aggressive engine"},
        "paper_adapter": {"ok": true, "value": "registered", "expected": "registered"}
    }
}
```

## Env File

Paper flags absent from `/opt/trading/.env`. Existing vars: `TV_PERF_HOST`, `TV_PERF_PORT`, `TV_PERF_SCHEME`, `TELEGRAM_ENABLED`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

## Router State

`/opt/trading/state/router_state.json`: `{"active_engine": "COINM_SHORT", "updated_at": "2026-02-22T17:24:30.856461+00:00"}`

## Ledger

No `ledger_paper.json` file exists.

## RISKS

- À qualifier.
