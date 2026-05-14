# GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_PNL_ALERT_THRESHOLDS_01

## Metadata

| Field | Value |
|-------|-------|
| scope | monitoring P&L + alert thresholds |
| type | doc-only |
| payload_sent | none |
| runtime_changes | none |
| live_trading_impact | none |

## Context

Monitoring condition was PARTIAL. This GO defines P&L tracking and alert thresholds to move towards SATISFIED.

## Objectives

1. Define P&L tracking specification
2. Define alert thresholds
3. Document monitoring gaps
4. Define validation plan
5. Do NOT open production

## Constraints

- Doc-only (or bounded runtime changes)
- No live trading
- No real orders
- No secrets in repo
- Production remains closed
