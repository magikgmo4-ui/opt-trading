---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_PLAN_01_PASS_WARN_FAIL_STOP
doc_type: pass_warn_fail_stop_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_PLAN_01
status: active
updated_at: 2026-05-13
---

# PASS_WARN_FAIL_STOP_MATRIX_01

| Result | Condition | Action |
| --- | --- | --- |
| PASS | errors=[], safety flags true, quotas OK, exit 0 | Continue monitoring |
| WARN | expected warnings only, single FAIL isolated | Observe reinforced |
| FAIL | errors non-empty, multiple consecutive FAIL, quota exceeded | Stop, investigate |
| STOP | safety flag false, kill-switch, secret leak | Immediate halt, rollback |

## Immediate STOP triggers

- `no_trade` becomes `false`
- `no_telegram` becomes `false`
- `no_webhook` becomes `false`
- `no_systemd` becomes `false`
- Quota exceeded
- Manual kill-switch
