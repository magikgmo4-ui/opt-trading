---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_CONTROLLED_PILOT_PLAN_01_STOP
doc_type: stop_rollback_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_CONTROLLED_PILOT_PLAN_01
status: active
updated_at: 2026-05-13
---

# STOP_ROLLBACK_MATRIX_01

| Condition | Severity | Action | Rollback needed |
| --- | --- | --- | --- |
| safety flag false | CRITICAL | Stop, investigate | YES |
| errors non-empty | HIGH | Stop if critical | Conditional |
| artifact missing | HIGH | Stop, investigate | YES |
| exit non-zero | HIGH | Stop | YES |
| 3 consecutive FAIL | MEDIUM | Stop, investigate | Conditional |
| single FAIL isolated | LOW | WARN, observe | NO |
| expected WARN only | INFO | Document | NO |

## Immediate STOP triggers

- `no_trade` becomes `false`
- `no_telegram` becomes `false`
- `no_webhook` becomes `false`
- `no_systemd` becomes `false`
- Secret appears in artifact or log
- Unexpected network call detected
