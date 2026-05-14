# 40_ALERT_THRESHOLDS_SPEC

## Alert Thresholds

| Alert | Threshold | Priority | Channel |
|-------|-----------|----------|---------|
| Daily loss exceeded | > 100 USD | P0 | Telegram |
| Max drawdown | > 10% | P0 | Telegram |
| Position limit reached | >= 3 | P1 | Telegram |
| Order rate limit | >= 10/hour | P1 | Telegram |
| Service down | inactive | P0 | Telegram |
| Guard failure | ok:false | P1 | Telegram |
| Kill switch activated | TRADE_ALLOWED=false | P0 | Telegram |
| Large trade | > 500 USD notional | P2 | Log |
| Stale position | > 24h open | P2 | Log |

## Alert Routing

| Priority | Channel | Frequency |
|----------|---------|-----------|
| P0 | Telegram + Log | Immediate |
| P1 | Telegram + Log | Immediate |
| P2 | Log only | Aggregated |

## Implementation Plan

### 1. Alert Configuration

File: `/opt/trading/state/alert_config.json`

```json
{
    "thresholds": {
        "daily_loss": 100,
        "max_drawdown_pct": 10,
        "max_positions": 3,
        "max_orders_per_hour": 10,
        "large_trade_notional": 500
    },
    "channels": {
        "telegram": {"enabled": true, "priorities": ["P0", "P1"]},
        "log": {"enabled": true, "priorities": ["P0", "P1", "P2"]}
    }
}
```

### 2. Alert Endpoint

```
GET /api/alerts
Response: {
    "ok": true,
    "active_alerts": [],
    "alert_history": [],
    "config": {...}
}
```

### 3. Alert Triggers

- **Pre-execution**: Check position limit, order rate
- **Post-execution**: Check trade size, daily P&L
- **Periodic**: Check service health, guard status
- **On state change**: Kill switch, guard failure

## Current State

- Alert configuration: NOT IMPLEMENTED
- Alert endpoint: NOT IMPLEMENTED
- Telegram alerts: AVAILABLE (basic)
- Alert thresholds: NOT CONFIGURED

## Status: SPECIFIED

Alert thresholds specified. Implementation required.
