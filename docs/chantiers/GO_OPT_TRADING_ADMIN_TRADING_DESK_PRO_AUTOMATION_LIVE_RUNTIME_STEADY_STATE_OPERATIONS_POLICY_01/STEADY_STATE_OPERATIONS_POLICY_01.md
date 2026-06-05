---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_STEADY_STATE_OPERATIONS_POLICY_01
doc_type: steady_state_operations_policy
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_STEADY_STATE_OPERATIONS_POLICY_01
status: active
updated_at: 2026-05-14
---

# STEADY_STATE_OPERATIONS_POLICY_01

## 1_INITIAL_NEED

Define steady-state operations policy for Desk Pro dry-run after Phase 2 stability gate CONTINUE.

## 6_FINAL_TARGET

Establish governance framework for indefinite Phase 2 operations.

## 7_CANONICAL_STATE

- Phase 2 execution: PASS
- Phase 2 stability gate: CONTINUE
- Active runtime: steady-state at Phase 2 quotas
- Safety: guards, kill-switch, STOP triggers intact

## 8_VALIDATED_PLAN

Docs-only operations policy. No runtime changes.

## 12_INVARIANTS

- No quota increases
- No guard/kill-switch/STOP trigger deactivation
- Audit trail remains active
- Periodic reviews required
- Any new expansion requires separate GO

## Active quotas

| Quota | Value | Review window |
| --- | --- | --- |
| Max runs/day | 288 | Daily |
| Max artifact size | 2GB | Weekly |
| Max FAIL/h | 2 | Per incident |
| Max history/day | 5000 lines | Daily |
| Review cadence | 14 days | Per cycle |

## Operations rules

### Pass condition
All quotas respected, errors=[], safety flags true.

### Warn condition
Expected warnings only (visual_context missing). Non-blocking.

### Fail condition
Errors non-empty, quota exceeded, consecutive FAILs.

### Stop condition
Safety flag false, kill-switch, secret leak, manual override.

### Hold condition
Any anomaly requiring investigation before continuing.

### Reduce condition
Quota consistently near limit, unexplained failures.

## Kill-switch policy

Always available. Activation conditions:
- Safety flag becomes false
- Quota exceeded
- Manual override
- 3 consecutive FAIL
- Secret leak

## Rollback policy

```bash
sudo systemctl disable --now desk_pro_dry_run.timer
sudo rm -f /etc/systemd/system/desk_pro_dry_run.service
sudo rm -f /etc/systemd/system/desk_pro_dry_run.timer
sudo systemctl daemon-reload
```

## Monitoring requirements

- `journalctl -u desk_pro_dry_run.service` per run
- `history.jsonl` for artifact trail
- `latest.json` for current state
- Report published every 14 days

## Expansion reopen criteria

- Minimum 30 days stable at Phase 2 quotas
- No STOP triggers in prior 30 days
- Safety flags true throughout
- All quotas respected
- Formal GO proposal with risk analysis

## RISKS

- À qualifier.
