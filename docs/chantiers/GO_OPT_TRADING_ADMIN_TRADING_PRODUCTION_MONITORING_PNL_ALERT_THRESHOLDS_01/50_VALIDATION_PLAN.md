# 50_VALIDATION_PLAN

## Validation Criteria

| Criteria | Check | Expected |
|----------|-------|----------|
| P&L tracking | GET /api/pnl | Returns daily/cumulative P&L |
| Alert thresholds | GET /api/alerts | Returns configured thresholds |
| Service health | systemctl is-active | All services active |
| Guard status | GET /api/paper/guards | Returns ok:true/false |
| Kill switch status | GET /api/risk/status | Returns trade_allowed |
| Telegram alerts | Test alert | Received in chat |

## Validation Steps

### Step 1: Verify P&L Tracking

```bash
curl -s http://127.0.0.1:8000/api/pnl | python3 -m json.tool
```

Expected: Returns P&L data (even if zero).

### Step 2: Verify Alert Thresholds

```bash
curl -s http://127.0.0.1:8000/api/alerts | python3 -m json.tool
```

Expected: Returns threshold configuration.

### Step 3: Verify Service Health

```bash
systemctl is-active tv-webhook.service tv-perf.service ngrok-tv.service
```

Expected: All return "active".

### Step 4: Verify Guard Status

```bash
curl -s http://127.0.0.1:8000/api/paper/guards | python3 -m json.tool
```

Expected: Returns guard status.

### Step 5: Verify Kill Switch Status

```bash
curl -s http://127.0.0.1:8000/api/risk/status | python3 -m json.tool
```

Expected: Returns trade_allowed status.

### Step 6: Verify Telegram Alerts

Send test alert and verify receipt.

## Pass Criteria

- All validation steps pass
- P&L tracking returns data
- Alert thresholds configured
- Services healthy
- Guards functional
- Kill switch visible

## Status: DEFINED

Validation plan defined. Execution pending implementation.
