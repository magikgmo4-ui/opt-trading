---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_PHASE_04_EXECUTION_PACKET
doc_type: execution_packet
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: active
---

# 99_PHASE_04_EXECUTION_PACKET

## Goal

Execute HITL approvals rollout: 7 jobs covering proposal, approval, preflight, verification, expiry, dual-confirm, pending-digest.

## Phase 04 exact jobs

| job_id | category | surface | mode | ready_now | action |
|---|---|---|---|---|---|
| `proposal-packet-create` | hitl | proposal | draft | partial | create proposal from template |
| `approval-packet-validate` | hitl | approval | read-only | yes | validate existing proposals |
| `execution-packet-preflight` | hitl | execution | read-only | yes | preflight readiness check |
| `verification-packet-create` | hitl | verification | report | partial | create verification template |
| `approval-expiry-check` | hitl | approvals queue | local write | yes | scan for expired approvals |
| `dual-confirm-required-check` | hitl | approval policy | read-only | yes | enforce dual confirm policy |
| `pending-approvals-digest` | hitl | approvals queue | report | yes | summarize pending items |

## Infrastructure notes

- Existing proposals: `data/canary/proposals/` (1 existing: `23ca9554216a.json`)
- Drafts: `data/drafts/` (3 entries)
- Kill switch: `data/kill_switch/` (3 entries)
- Scheduler: `data/scheduler/alerts/`, `dead_letter/`, `jobs/`
- Proposal schema: `proposal_id`, `action`, `description`, `risk`, `target`, `reversible`, `critical`, `status`, `confirmations`, `confirm_count`, `confirm_required`
- Dual confirm requires 2 HUMAN confirmations (`human_01`, `human_02`)
- HITL gate defined in `50_KILL_SWITCH_LEDGER_HITL_POLICY.md`

## Execution order

### Phase 04A: Validation & audit (ready now)

1. `approval-packet-validate`
2. `execution-packet-preflight`
3. `dual-confirm-required-check`
4. `approval-expiry-check`
5. `pending-approvals-digest`

### Phase 04B: Create (helper needed)

6. `proposal-packet-create`
7. `verification-packet-create`
