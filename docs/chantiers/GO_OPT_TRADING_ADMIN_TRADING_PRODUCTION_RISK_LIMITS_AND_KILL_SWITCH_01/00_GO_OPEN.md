# GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01

## Metadata

| Field | Value |
|-------|-------|
| scope | risk limits + kill switch |
| type | doc-only |
| payload_sent | none |
| runtime_changes | none |
| live_trading_impact | none |

## Context

Production readiness conditions defined in PR #388. Risk limits and kill switch are structuring prerequisites. This GO specifies them without implementing or activating production.

## Objectives

1. Define minimum risk limits
2. Specify kill switch mechanism
3. Document rollback plan
4. Define validation gates
5. Do NOT open production

## Constraints

- Doc-only
- No live trading
- No real orders
- No runtime changes
- No secrets
- Production remains closed
