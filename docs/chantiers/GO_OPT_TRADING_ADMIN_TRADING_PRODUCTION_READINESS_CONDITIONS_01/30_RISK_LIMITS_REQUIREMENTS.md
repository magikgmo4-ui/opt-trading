# 30_RISK_LIMITS_REQUIREMENTS

## Current State

No risk limits defined for production trading.

## Required Limits

| Limit | Description | Current | Required |
|-------|-------------|---------|----------|
| Max position size | Maximum qty per trade | unlimited | define |
| Max loss per trade | Stop loss mandatory | optional | mandatory |
| Max daily loss | Daily loss cap | none | define |
| Max open positions | Concurrent positions | unlimited | define |
| Max notional | Total exposure | unlimited | define |

## Recommendations

1. **Position size**: Max 1% of portfolio per trade
2. **Stop loss**: Mandatory, max 2% loss per trade
3. **Daily loss**: Max 5% of portfolio
4. **Open positions**: Max 3 concurrent
5. **Notional**: Max 10% of portfolio total exposure

## Implementation

- Add risk limits to `/opt/trading/.env`
- Implement in webhook_server.py risk_quote()
- Enforce before execution
- Log all limit breaches

## Status: MISSING

No limits defined. Must be implemented before production.
