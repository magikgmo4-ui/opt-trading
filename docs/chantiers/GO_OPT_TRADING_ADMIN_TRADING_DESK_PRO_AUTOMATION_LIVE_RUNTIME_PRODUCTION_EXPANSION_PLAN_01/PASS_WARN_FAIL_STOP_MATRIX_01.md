---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PLAN_01_STOP_MATRIX
doc_type: pass_warn_fail_stop_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PLAN_01
status: active
updated_at: 2026-05-13
---

# PASS_WARN_FAIL_STOP_MATRIX_01

| Result | Condition | Action |
| --- | --- | --- |
| PASS | errors=[], safety flags true, quotas OK, exit 0 | Continue monitoring |
| WARN | expected warnings only, isolated FAIL | Observe reinforced |
| FAIL | errors non-empty, multiple consecutive FAIL, quota breached | Stop, investigate |
| STOP | safety flag false, kill-switch, secret leak | Immediate halt, rollback |

## Immediate STOP triggers

- `no_trade` becomes `false`
- `no_telegram` becomes `false`
- `no_webhook` becomes `false`
- `no_systemd` becomes `false`
- Quota exceeded
- Manual kill-switch
