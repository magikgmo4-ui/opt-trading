# 20_RISK_LIMITS_SPEC

## Minimum Risk Limits for Production

| Limit | Value | Enforcement | Status |
|-------|-------|-------------|--------|
| Max notional per trade | 1000 USD | pre-execution check | TO IMPLEMENT |
| Max position size | 0.01 BTC / 0.1 ETH | pre-execution check | TO IMPLEMENT |
| Max daily loss | 100 USD (10% of 1000) | daily tracker | TO IMPLEMENT |
| Max open positions | 3 | position counter | TO IMPLEMENT |
| Max orders per hour | 10 | rate limiter | TO IMPLEMENT |
| Allowed symbols | BTC/USDT, ETH/USDT | whitelist | TO IMPLEMENT |
| Allowed engines | PAPER_TEST, LIVE_PROD | whitelist | TO IMPLEMENT |
| Paper/live separation | mandatory | env-based gate | PARTIAL |

## Current State

| Limit | Current | Gap |
|-------|---------|-----|
| Max notional | unlimited | MISSING |
| Max position size | unlimited | MISSING |
| Max daily loss | none | MISSING |
| Max open positions | unlimited | MISSING |
| Max orders per hour | none | MISSING |
| Allowed symbols | all | MISSING |
| Allowed engines | all registered | OK |
| Paper/live separation | TRADE_ALLOWED=false | PARTIAL |

## Implementation Plan

### 1. Environment Variables

```bash
# /opt/trading/.env
RISK_MAX_NOTIONAL=1000
RISK_MAX_POSITION_SIZE_BTC=0.01
RISK_MAX_POSITION_SIZE_ETH=0.1
RISK_MAX_DAILY_LOSS=100
RISK_MAX_OPEN_POSITIONS=3
RISK_MAX_ORDERS_PER_HOUR=10
RISK_ALLOWED_SYMBOLS=BTC/USDT,ETH/USDT
```

### 2. Enforcement Points

- **Pre-execution**: Check in webhook_server.py before executor.execute()
- **Daily tracker**: Track daily P&L in state/daily_pnl.json
- **Rate limiter**: Track orders in state/order_count.json

### 3. Rejection Behavior

When limit breached:
- HTTP 429 (rate limit) or HTTP 400 (limit exceeded)
- Log breach event
- Send Telegram alert if configured
- No execution

## Decision

**PARTIAL** — Limits specified but not implemented. Implementation required before production.
