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
- `hitl-scenarios-smoke`
- `localcms-automation-status-sync`

Verdict: `PHASE_01_EXECUTED`
Count: `12 jobs`

Execution result:

- `11 PASS`
- `1 PRECHECK_PASS`
- `0 FAIL`

Gate commun avant activation:

- aucun write externe requis
- ledger actif et replay verifiable
- outputs report/local-only bornes
- aucun lien signal/trading

### Phase 02

Repo/docs/governance and strict-workers hardening:

- `repo-branch-audit`
- `repo-go-index-audit`
- `repo-doc-frontmatter-lint`
- `repo-doc-link-check`
- `repo-closeout-eligibility-check`
- `repo-parent-coverage-board-refresh`
- `repo-memory-bricks-candidate-scan`
- `repo-changelog-digest`
- `repo-orphan-files-audit`
- `repo-scope-guard`
- `repo-pr-review-preflight`
- `repo-release-note-draft`
- `strict-worker-model-registry-check`
- `strict-worker-task-index-check`
- `strict-worker-job-packet-validate`
- `strict-worker-output-schema-check`
- `strict-worker-denied-command-scan`
- `strict-worker-log-archive`
- `strict-worker-failure-report`

Verdict: `PHASE_02_SELECTED`
Count: `19 jobs`

Scope:

- repo/docs/governance extended jobs
- strict-workers validation and archive layer

### Phase 03

Ledger and security hardening:

- `ledger-blocked-events-digest`
- `ledger-rotation-check`
- `ledger-schema-validation`
- `ledger-trace-id-audit`
- `automation-health-digest`
- `kill-switch-state-check`
- `stuck-job-detector`
- `env-file-presence-check`
- `gitignore-secrets-policy-check`
- `oauth-scope-audit`
- `external-token-presence-check`
- `permission-drift-check`
- `kill-switch-fullstop-test`
- `deny-by-default-check`

Verdict: `PHASE_03_EXECUTED`
Count: `14 jobs`
Execution result:
- `13 PASS`
- `1 WARN`
- `0 FAIL`
Gate: `PASS_WITH_FINDINGS`

### Phase 04

HITL approvals rollout:

- `proposal-packet-create`
- `approval-packet-validate`
- `execution-packet-preflight`
- `verification-packet-create`
- `approval-expiry-check`
- `dual-confirm-required-check`
- `pending-approvals-digest`

Verdict: `PHASE_04_EXECUTED`
Count: `7 jobs`
Execution result:
- `7 PASS`
- `0 WARN`
- `0 FAIL`
Gate: `PASS`

### Phase 05

Capability matrix and AI-team rollout:

- `capability-drift-check`
- `ai-team-role-registry-check`
- `handoff-packet-schema-check`
- `memory-broker-dry-run`
- `task-router-dry-run`
- `handoff-timeout-check`

Verdict: `PHASE_05_EXECUTED`
Count: `6 jobs`
Execution result:
- `4 PASS`
- `2 WARN`
- `0 FAIL`
Gate: `PASS_WITH_FINDINGS`

### Phase 06

LocalCMS cockpit rollout:

- `localcms-static-cockpit-build`
- `localcms-workers-state-sync`
- `localcms-jobs-queue-sync`
- `localcms-approvals-sync`
- `localcms-ledger-view-refresh`
- `localcms-safe-buttons-check`
- `localcms-kill-switch-widget-check`

Verdict: `PHASE_06_EXECUTED`
Count: `7 jobs`
Execution result:
- `5 PASS`
- `2 WARN`
- `0 FAIL`
Gate: `PASS_WITH_FINDINGS`

### Phase 07

External apps read and contract baseline:

- `airtable-read-health`
- `airtable-contract-check`
- `clickup-read-health`
- `clickup-contract-check`
- `botpress-read-health`
- `botpress-contract-check`
- `kg-repo-read-index`
- `kg-repo-drift-check`
- `kg-repo-orphan-node-audit`
- `sheets-read-health`
- `gmail-read-report-inbox`
- `calendar-read-automation-events`
- `drive-read-folder-health`

Verdict: `PHASE_07_EXECUTED`
Count: `13 jobs`
Execution result:
- `9 PASS`
- `4 WARN`
- `0 FAIL`
Gate: `PASS_WITH_FINDINGS`

### Phase 08

External apps canary and write-gated rollout:

- `airtable-canary-proposal`
- `airtable-canary-write`
- `airtable-readback-verify`
- `airtable-snapshot-before-write`
- `airtable-rollback-verify`
- `clickup-canary-proposal`
- `clickup-canary-task-create`
- `clickup-task-readback-verify`
- `clickup-task-update-canary`
- `clickup-compensation-note`
- `botpress-dev-message-proposal`
- `botpress-dev-message-send`
- `botpress-variable-update-canary`
- `botpress-readback-verify`
- `kg-repo-node-proposal`
- `kg-repo-pr-gated-sync`
- `kg-repo-readback-verify`
- `sheets-report-export-proposal`
- `sheets-canary-cell-write`
- `sheets-readback-verify`
- `sheets-snapshot-before-write`
- `telegram-notification-health`
- `telegram-automation-digest`
- `telegram-blocked-events-alert`
- `telegram-approval-reminder`
- `gmail-draft-report`
- `calendar-create-review-event`
- `drive-upload-report-canary`

Verdict: `PHASE_08_EXECUTED`
Count: `28 jobs`
Execution result:
- `25 PASS`
- `3 WARN`
- `0 FAIL`
Gate: `PASS_WITH_FINDINGS`

### Phase 09

Scheduler and CI activation:

- `scheduler-config-validate`
- `scheduler-unit-lint`
- `scheduler-user-timers-list`
- `scheduler-dead-letter-check`
- `scheduler-retry-policy-check`
- `scheduler-dry-run-next-fire`
- `ci-nightly-validation`
- `ci-status-ingest`

Verdict: `PHASE_09_EXECUTED`
Count: `8 jobs`
Execution result:
- `8 PASS`
- `0 WARN`
- `0 FAIL`
Gate: `PASS`

## Source priorisee

Cette priorisation reprend la liste maitre validee dans `7_CANONICAL_STATE`.

## Gates

- Phase 01 : read-only / dry-run / local-only
- Phase 02 : write-gated + readback + rollback
- Phase 03 : scheduler config validated + dead-letter active + alerting active
