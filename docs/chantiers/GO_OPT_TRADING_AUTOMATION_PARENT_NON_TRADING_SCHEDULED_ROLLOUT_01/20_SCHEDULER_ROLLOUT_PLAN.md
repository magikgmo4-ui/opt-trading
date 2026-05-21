---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_SCHEDULER_ROLLOUT_PLAN
doc_type: rollout_plan
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: draft
---

# 20_SCHEDULER_ROLLOUT_PLAN

## Phases

### Phase 01

Jobs immediats, lecture seule ou local write non critique:

- `repo-status-check`
- `repo-diff-check`
- `repo-pr-audit`
- `automation-health-status`
- `ledger-heartbeat`
- `ledger-replay-check`
- `anti-leak-scan`
- `strict-worker-readonly-smoke`
- `capability-matrix-validate`
- `ai-team-handoff-dry-run`
- `bridge-contract-validation`
- `hitl-scenarios-smoke`
- `localcms-automation-status-sync`

### Phase 02

Canaries apps externes sous write-gated:

- `clickup-canary-task-create`
- `airtable-canary-write`
- `botpress-dev-message-send`
- `kg-repo-pr-gated-sync`
- `telegram-automation-digest`

### Phase 03

Timers reels de scheduler:

- `scheduler-user-timers-list`
- `automation-health-status.timer`
- `automation-ledger-heartbeat.timer`
- `automation-nightly-validation.timer`
- `external-apps-canary.timer`

## Source priorisee

Cette priorisation reprend la liste maitre validee dans `7_CANONICAL_STATE`.

## Gates

- Phase 01 : read-only / dry-run / local-only
- Phase 02 : write-gated + readback + rollback
- Phase 03 : scheduler config validated + dead-letter active + alerting active
