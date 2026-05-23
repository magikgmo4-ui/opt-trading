---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_PHASE_03_EXECUTION_PACKET
doc_type: execution_packet
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: active
---

# 96_PHASE_03_EXECUTION_PACKET

## Goal

Execute ledger/security hardening wave: 14 jobs (7 ledger + 7 security).

## Phase 03 exact jobs

| job_id | category | surface | mode | ready_now | action |
|---|---|---|---|---|---|
| `ledger-blocked-events-digest` | ledger | ledger | read-only/report | helper | tiny helper |
| `ledger-rotation-check` | ledger | ledger archive | local write archive | helper | tiny helper |
| `ledger-schema-validation` | ledger | ledger | read-only | helper | tiny helper |
| `ledger-trace-id-audit` | ledger | ledger | read-only | helper | tiny helper |
| `automation-health-digest` | ledger | health summary | report | yes | parse latest.json |
| `kill-switch-state-check` | ledger | kill switch | read-only | yes | cat kill_switch.state |
| `stuck-job-detector` | ledger | scheduler state | read-only/report | helper | tiny helper |
| `env-file-presence-check` | security | `.env*` | read-only | yes | find .env* |
| `gitignore-secrets-policy-check` | security | `.gitignore` | read-only | yes | grep .gitignore |
| `oauth-scope-audit` | security | app scopes | read-only/report | helper | tiny helper |
| `external-token-presence-check` | security | env vars | read-only | manual | manual check |
| `permission-drift-check` | security | permissions | read-only/report | helper | tiny helper |
| `kill-switch-fullstop-test` | security | kill switch | dry-run | manual | manual dry-run |
| `deny-by-default-check` | security | write gates | dry-run | manual | manual dry-run |

## Summary

- Ready now: `4/14`
- Tiny helper needed: `7/14`
- Manual: `3/14`

## Infrastructure notes

- Ledger is `data/runtime_health/` (healthcheck.jsonl + latest.json + kill_switch.state)
- No separate `data/ledger/` directory exists — ledger = runtime health system
- `data/runtime_health/healthcheck.jsonl`: 902 entries, all `PASS`
- `data/runtime_health/latest.json`: current snapshot (overall_status: PASS)
- `data/runtime_health/kill_switch.state`: "NORMAL"

## Recommended execution order

### Phase 03A: Ready-now set

1. `kill-switch-state-check`
2. `automation-health-digest`
3. `env-file-presence-check`
4. `gitignore-secrets-policy-check`

### Phase 03B: Tiny helpers

5. `ledger-blocked-events-digest`
6. `ledger-rotation-check`
7. `ledger-schema-validation`
8. `ledger-trace-id-audit`
9. `stuck-job-detector`
10. `oauth-scope-audit`
11. `permission-drift-check`

### Phase 03C: Manual

12. `external-token-presence-check`
13. `kill-switch-fullstop-test`
14. `deny-by-default-check`
