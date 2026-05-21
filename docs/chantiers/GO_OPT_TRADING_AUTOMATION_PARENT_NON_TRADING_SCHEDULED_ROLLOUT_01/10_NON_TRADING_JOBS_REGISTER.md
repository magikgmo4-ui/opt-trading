---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_NON_TRADING_JOBS_REGISTER
doc_type: jobs_register
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: active
---

# 10_NON_TRADING_JOBS_REGISTER

## Schema canonique

```text
job_id
category
surface
script_or_tool
mode
allowed_writes
gate
scheduler
frequency
evidence_required
status
```

## Statuts utilises

- `phase_01_selected` : baseline immediate read-only / dry-run / local-only
- `phase_02_selected` : repo/docs/strict-workers governance hardening
- `phase_03_selected` : ledger/security hardening
- `phase_04_selected` : HITL approvals rollout
- `phase_05_selected` : capability matrix / AI-team rollout
- `phase_06_selected` : LocalCMS cockpit rollout
- `phase_07_selected` : external apps read/contract baseline
- `phase_08_selected` : external apps canary/write-gated rollout
- `phase_09_selected` : scheduler/CI activation

## A. Repo / Git / docs

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `repo-status-check` | repo | git | `git status` | read-only | none | none | enabled | 15 min | branch clean report | phase_01_selected |
| `repo-diff-check` | repo | repo | `git diff --check` | read-only | none | none | enabled | 30 min | whitespace/conflict report | phase_01_selected |
| `repo-branch-audit` | repo | git | `git branch`/`gh` | read-only | none | none | enabled | daily | merged/orphan branch report | phase_02_selected |
| `repo-pr-audit` | repo | github | `gh pr list` | read-only | none | none | enabled | hourly | PR state digest | phase_01_selected |
| `repo-go-index-audit` | repo | docs index | index audit runner | read-only | none | none | enabled | daily | chantier + inbox audit | phase_02_selected |
| `repo-doc-frontmatter-lint` | repo | docs | frontmatter lint | read-only/report | none | none | enabled | daily | lint report | phase_02_selected |
| `repo-doc-link-check` | repo | docs | link checker | read-only/report | none | none | enabled | daily | link report | phase_02_selected |
| `repo-closeout-eligibility-check` | repo | governance docs | closeout audit | read-only | none | none | enabled | daily | closable GO report | phase_02_selected |
| `repo-parent-coverage-board-refresh` | repo | parent board | board refresh generator | draft only | draft docs only | HITL | manual | manual/HITL | proposed board patch | phase_02_selected |
| `repo-memory-bricks-candidate-scan` | repo | docs memory | scan runner | read-only/draft | draft docs only | none | enabled | daily | candidate list | phase_02_selected |
| `repo-changelog-digest` | repo | git/github | changelog digest runner | read-only/report | none | none | enabled | daily | digest report | phase_02_selected |
| `repo-orphan-files-audit` | repo | repo fs | orphan audit runner | read-only | none | none | enabled | daily | orphan file report | phase_02_selected |
| `repo-scope-guard` | repo | diff scope | scope guard | read-only | none | none | enabled | pre-commit/manual | out-of-scope report | phase_02_selected |
| `repo-pr-review-preflight` | repo | PR review | preflight runner | read-only | none | none | manual | manual | preflight checklist | phase_02_selected |
| `repo-release-note-draft` | repo | docs/release | release note generator | draft only | draft docs only | HITL | manual | manual/HITL | draft note | phase_02_selected |

## B. Strict workers

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `strict-worker-model-registry-check` | workers | worker registry | `models.registry.json` validator | read-only | none | none | enabled | daily | registry validation PASS | phase_02_selected |
| `strict-worker-task-index-check` | workers | task index | `tasks.index.json` validator | read-only | none | none | enabled | daily | task index validation PASS | phase_02_selected |
| `strict-worker-job-packet-validate` | workers | job packets | packet validator | read-only | none | none | on demand | on demand | packet validation report | phase_02_selected |
| `strict-worker-readonly-smoke` | workers | worker runtime | readonly smoke runner | read-only + reports | reports only | readonly guard | enabled | 6 h | smoke PASS report | phase_01_selected |
| `strict-worker-output-schema-check` | workers | worker outputs | schema check runner | read-only | none | none | after run | after run | output schema PASS | phase_02_selected |
| `strict-worker-denied-command-scan` | workers | worker logs | denied command scan | read-only | none | none | after run | after run | no forbidden command report | phase_02_selected |
| `strict-worker-log-archive` | workers | logs | log archiver | local write logs | local logs only | local-only | enabled | daily | archive artifact | phase_02_selected |
| `strict-worker-failure-report` | workers | failures | failure reporter | report | reports only | none | on failure | on failure | FAIL/BLOCKED report | phase_02_selected |

## C. Ledger / observabilite

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `ledger-heartbeat` | ledger | ledger | heartbeat writer | local write ledger | ledger only | local-only | enabled | 15 min | heartbeat event present | phase_01_selected |
| `ledger-replay-check` | ledger | ledger | replay checker | read-only | none | none | enabled | hourly | replay order PASS | phase_01_selected |
| `ledger-blocked-events-digest` | ledger | ledger | digest runner | read-only/report | reports only | none | enabled | hourly | BLOCKED/FAIL digest | phase_03_selected |
| `ledger-rotation-check` | ledger | ledger archive | rotation checker | local write archive | archive only | local-only | enabled | daily | rotation/archive report | phase_03_selected |
| `ledger-schema-validation` | ledger | ledger | schema validator | read-only | none | none | enabled | hourly | schema PASS | phase_03_selected |
| `ledger-trace-id-audit` | ledger | ledger | trace audit | read-only | none | none | enabled | daily | trace_id coverage report | phase_03_selected |
| `automation-health-status` | ledger | local report | status generator | local write report | report only | local-only | enabled | 15 min | `health_status.json` updated | phase_01_selected |
| `automation-health-digest` | ledger | health summary | digest runner | report | reports only | none | enabled | hourly | health digest | phase_03_selected |
| `kill-switch-state-check` | ledger | kill switch | state checker | read-only | none | none | enabled | 5 min | kill switch state report | phase_03_selected |
| `stuck-job-detector` | ledger | scheduler state | stuck job scan | read-only/report | reports only | none | enabled | 15 min | stuck job report | phase_03_selected |

## D. Securite / secrets / permissions

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `anti-leak-scan` | security | outputs | secret scan | read-only | none | none | enabled | 6 h | no secret report | phase_01_selected |
| `env-file-presence-check` | security | `.env*` | env audit | read-only | none | none | enabled | daily | env presence report | phase_03_selected |
| `gitignore-secrets-policy-check` | security | `.gitignore` | policy check | read-only | none | none | enabled | daily | policy PASS | phase_03_selected |
| `oauth-scope-audit` | security | app scopes | scope audit | read-only/report | reports only | none | enabled | daily | scope drift report | phase_03_selected |
| `external-token-presence-check` | security | env vars | token presence checker | read-only | none | none | manual/daily | manual/daily | required vars present | phase_03_selected |
| `permission-drift-check` | security | permissions | drift audit | read-only/report | reports only | none | enabled | daily | drift report | phase_03_selected |
| `kill-switch-fullstop-test` | security | kill switch | dry-run test | dry-run | none | dry-run guard | manual | manual | controlled test PASS | phase_03_selected |
| `deny-by-default-check` | security | write gates | policy test | dry-run | none | deny-by-default | enabled | daily | blocked write proof | phase_03_selected |

## E. HITL / approvals

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `proposal-packet-create` | hitl | proposal | proposal generator | draft | draft packets only | HITL | on demand | on demand | proposal packet | phase_04_selected |
| `approval-packet-validate` | hitl | approval | approval validator | read-only | none | none | on demand | on demand | approval validity PASS | phase_04_selected |
| `execution-packet-preflight` | hitl | execution | preflight runner | read-only | none | none | on demand | on demand | preflight PASS | phase_04_selected |
| `verification-packet-create` | hitl | verification | verification generator | report | reports only | none | after action | after action | verification packet | phase_04_selected |
| `approval-expiry-check` | hitl | approvals queue | expiry checker | local write status | approval status only | local-only | enabled | hourly | expired approvals updated | phase_04_selected |
| `dual-confirm-required-check` | hitl | approval policy | dual confirm checker | read-only | none | none | on demand | on demand | dual confirm enforced | phase_04_selected |
| `hitl-scenarios-smoke` | hitl | HITL flows | scenario smoke runner | dry-run | none | dry-run guard | enabled | nightly | scenario PASS report | phase_01_selected |
| `pending-approvals-digest` | hitl | approvals queue | digest runner | report | reports only | none | enabled | hourly | pending approvals digest | phase_04_selected |

## F. Capability matrix / AI team

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `capability-matrix-validate` | ai-team | capability matrix | matrix validator | read-only | none | none | enabled | nightly | matrix PASS | phase_01_selected |
| `capability-drift-check` | ai-team | app/job mapping | drift checker | read-only/report | reports only | none | enabled | daily | drift report | phase_05_selected |
| `ai-team-handoff-dry-run` | ai-team | handoff | dry-run | none | dry-run guard | enabled | nightly | handoff PASS report | phase_01_selected |
| `ai-team-role-registry-check` | ai-team | role registry | registry checker | read-only | none | none | enabled | daily | role registry PASS | phase_05_selected |
| `handoff-packet-schema-check` | ai-team | handoff packet | schema checker | read-only | none | none | on demand | on demand | schema PASS | phase_05_selected |
| `memory-broker-dry-run` | ai-team | shared memory | dry-run/local | local memory only | dry-run guard | enabled | nightly | dry-run PASS | phase_05_selected |
| `task-router-dry-run` | ai-team | task router | dry-run router | dry-run | none | dry-run guard | enabled | nightly | routing PASS | phase_05_selected |
| `handoff-timeout-check` | ai-team | handoff queue | timeout checker | read-only/report | reports only | none | enabled | hourly | timeout report | phase_05_selected |

## G. LocalCMS / cockpit

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `localcms-static-cockpit-build` | cockpit | localcms build | static builder | local write build | local build only | local-only | on change | on change | build artifact | phase_06_selected |
| `localcms-automation-status-sync` | cockpit | localcms status | sync runner | write-gated/local | local rendered views only | local gate | enabled | 30 min | status sync artifact | phase_01_selected |
| `localcms-workers-state-sync` | cockpit | worker state | sync runner | write-gated/local | local rendered views only | local gate | enabled | 30 min | worker state artifact | phase_06_selected |
| `localcms-jobs-queue-sync` | cockpit | jobs queue | sync runner | write-gated/local | local rendered views only | local gate | enabled | 30 min | queue artifact | phase_06_selected |
| `localcms-approvals-sync` | cockpit | approvals | sync runner | write-gated/local | local rendered views only | local gate | enabled | 15 min | approvals artifact | phase_06_selected |
| `localcms-ledger-view-refresh` | cockpit | ledger view | refresh runner | read/local write view | local rendered views only | local gate | enabled | 15 min | ledger view refreshed | phase_06_selected |
| `localcms-safe-buttons-check` | cockpit | UI safety | UI checker | read-only | none | none | enabled | daily | safe button report | phase_06_selected |
| `localcms-kill-switch-widget-check` | cockpit | kill switch widget | UI checker | read-only | none | none | enabled | daily | widget report | phase_06_selected |

## H. Apps externes

### Airtable

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `airtable-read-health` | app-bridge | airtable | bridge contract | read-only | none | contract | enabled | hourly | read health PASS | phase_07_selected |
| `airtable-contract-check` | app-bridge | airtable | contract validator | read-only | none | contract | enabled | daily | contract PASS | phase_07_selected |
| `airtable-canary-proposal` | app-bridge | airtable | proposal runner | draft | draft only | HITL | manual | manual | proposal packet | phase_08_selected |
| `airtable-canary-write` | app-bridge | airtable | write-gated bridge | write-gated | canary record only | dual confirm | manual puis daily | manual/daily | write + readback proof | phase_08_selected |
| `airtable-readback-verify` | app-bridge | airtable | verify runner | read-only | none | none | after write | after write | readback PASS | phase_08_selected |
| `airtable-snapshot-before-write` | app-bridge | airtable | snapshot runner | local/app read | local snapshot only | before write | before write | before write | snapshot captured | phase_08_selected |
| `airtable-rollback-verify` | app-bridge | airtable | rollback checker | read-only | none | none | after write | after write | rollback feasibility PASS | phase_08_selected |

### ClickUp

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `clickup-read-health` | app-bridge | clickup | bridge contract | read-only | none | contract | enabled | hourly | read health PASS | phase_07_selected |
| `clickup-contract-check` | app-bridge | clickup | contract validator | read-only | none | contract | enabled | daily | contract PASS | phase_07_selected |
| `clickup-canary-proposal` | app-bridge | clickup | proposal runner | draft | draft only | HITL | manual | manual | proposal packet | phase_08_selected |
| `clickup-canary-task-create` | app-bridge | clickup | write-gated bridge | write-gated | canary task only | dual confirm | manual puis daily | manual/daily | create + readback proof | phase_08_selected |
| `clickup-task-readback-verify` | app-bridge | clickup | verify runner | read-only | none | none | after write | after write | readback PASS | phase_08_selected |
| `clickup-task-update-canary` | app-bridge | clickup | write-gated bridge | write-gated | canary field/comment only | dual confirm | manual | manual | update + readback proof | phase_08_selected |
| `clickup-compensation-note` | app-bridge | clickup | compensation runner | write-gated | compensation note only | HITL | after write | after write | compensation logged | phase_08_selected |

### Botpress

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `botpress-read-health` | app-bridge | botpress | bridge contract | read-only | none | contract | enabled | hourly | read health PASS | phase_07_selected |
| `botpress-contract-check` | app-bridge | botpress | contract validator | read-only | none | contract | enabled | daily | contract PASS | phase_07_selected |
| `botpress-dev-message-proposal` | app-bridge | botpress | proposal runner | draft | draft only | HITL | manual | manual | proposal packet | phase_08_selected |
| `botpress-dev-message-send` | app-bridge | botpress | write-gated bridge | write-gated | dev test message only | dual confirm | manual | manual | send + readback proof | phase_08_selected |
| `botpress-variable-update-canary` | app-bridge | botpress | write-gated bridge | write-gated | controlled variable only | dual confirm | manual | manual | update + readback proof | phase_08_selected |
| `botpress-readback-verify` | app-bridge | botpress | verify runner | read-only | none | none | after write | after write | readback PASS | phase_08_selected |

### KG Repo

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `kg-repo-read-index` | app-bridge | repo kg | kg reader | read-only | none | none | enabled | hourly/daily | index read PASS | phase_07_selected |
| `kg-repo-drift-check` | app-bridge | repo kg | drift checker | read-only | none | none | enabled | daily | drift report | phase_07_selected |
| `kg-repo-node-proposal` | app-bridge | repo kg | proposal runner | draft | draft only | HITL | enabled | daily | proposal packet | phase_08_selected |
| `kg-repo-pr-gated-sync` | app-bridge | repo kg | PR workflow | PR-gated | PR only | PR review | manual | manual | merged PR proof | phase_08_selected |
| `kg-repo-readback-verify` | app-bridge | repo kg | verify runner | read-only | none | none | after PR | after PR | readback PASS | phase_08_selected |
| `kg-repo-orphan-node-audit` | app-bridge | repo kg | orphan audit | read-only/report | reports only | none | enabled | daily | orphan node report | phase_07_selected |

### Google Sheets

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `sheets-read-health` | app-bridge | google sheets | bridge contract | read-only | none | contract | enabled | hourly | read health PASS | phase_07_selected |
| `sheets-report-export-proposal` | app-bridge | google sheets | proposal runner | draft | draft only | HITL | manual | manual | proposal packet | phase_08_selected |
| `sheets-canary-cell-write` | app-bridge | google sheets | write-gated bridge | write-gated | canary range only | dual confirm | manual | manual | write + readback proof | phase_08_selected |
| `sheets-readback-verify` | app-bridge | google sheets | verify runner | read-only | none | none | after write | after write | readback PASS | phase_08_selected |
| `sheets-snapshot-before-write` | app-bridge | google sheets | snapshot runner | read-only/local | local snapshot only | before write | before write | before write | snapshot captured | phase_08_selected |

### Telegram non-trading

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `telegram-notification-health` | app-bridge | telegram | notifier | write notification | notification only | notification policy | manual/daily | manual/daily | delivery proof | phase_08_selected |
| `telegram-automation-digest` | app-bridge | telegram | digest sender | notification only | notification only | notification policy | enabled | daily | digest delivered | phase_08_selected |
| `telegram-blocked-events-alert` | app-bridge | telegram | alert sender | notification only | notification only | alert policy | on failure | on failure | alert delivered | phase_08_selected |
| `telegram-approval-reminder` | app-bridge | telegram | reminder sender | notification only | notification only | notification policy | enabled | hourly | reminder delivered | phase_08_selected |

### Gmail / Calendar / Drive

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `gmail-read-report-inbox` | app-bridge | gmail | bridge contract | read-only | none | contract | enabled | daily | read PASS | phase_07_selected |
| `gmail-draft-report` | app-bridge | gmail | draft generator | write-gated/draft | draft only | HITL | manual | manual | draft created | phase_08_selected |
| `calendar-read-automation-events` | app-bridge | calendar | bridge contract | read-only | none | contract | enabled | daily | read PASS | phase_07_selected |
| `calendar-create-review-event` | app-bridge | calendar | write-gated bridge | write-gated | review event only | dual confirm | manual | manual | event created | phase_08_selected |
| `drive-read-folder-health` | app-bridge | drive | bridge contract | read-only | none | contract | enabled | daily | read PASS | phase_07_selected |
| `drive-upload-report-canary` | app-bridge | drive | write-gated bridge | write-gated | canary upload only | dual confirm | manual | manual | upload proof | phase_08_selected |

## I. Scheduler / CI

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `scheduler-config-validate` | scheduler | scheduler config | config validator | read-only | none | none | on change | on change | config PASS | phase_09_selected |
| `scheduler-unit-lint` | scheduler | `.service/.timer` | unit lint | read-only | none | none | on change | on change | unit lint PASS | phase_09_selected |
| `scheduler-user-timers-list` | scheduler | timers | timers list runner | read-only | none | none | enabled | hourly | timers inventory | phase_09_selected |
| `scheduler-dry-run-next-fire` | scheduler | timer schedule | next-fire calculator | read-only | none | none | enabled | daily | next fire report | phase_09_selected |
| `scheduler-dead-letter-check` | scheduler | dead-letter queue | queue reader | read-only | none | none | enabled | hourly | dead-letter report | phase_09_selected |
| `scheduler-retry-policy-check` | scheduler | retry policy | policy validator | read-only | none | none | enabled | daily | retry policy PASS | phase_09_selected |
| `ci-nightly-validation` | scheduler | CI | validation workflow | CI/local | CI artifacts only | CI policy | enabled | nightly | CI PASS | phase_09_selected |
| `ci-status-ingest` | scheduler | CI status | ingest runner | write-gated/local | local status only | local gate | enabled | hourly | status ingest artifact | phase_09_selected |

## Priorisation pour utilisation reelle

| Phase | Nombre de jobs | Reference detaillee |
|---|---:|---|
| phase_01_selected | 12 | `20_SCHEDULER_ROLLOUT_PLAN.md#phase-01` |
| phase_02_selected | 19 | `20_SCHEDULER_ROLLOUT_PLAN.md#phase-02` |
| phase_03_selected | 14 | `20_SCHEDULER_ROLLOUT_PLAN.md#phase-03` |
| phase_04_selected | 7 | `20_SCHEDULER_ROLLOUT_PLAN.md#phase-04` |
| phase_05_selected | 6 | `20_SCHEDULER_ROLLOUT_PLAN.md#phase-05` |
| phase_06_selected | 7 | `20_SCHEDULER_ROLLOUT_PLAN.md#phase-06` |
| phase_07_selected | 13 | `20_SCHEDULER_ROLLOUT_PLAN.md#phase-07` |
| phase_08_selected | 28 | `20_SCHEDULER_ROLLOUT_PLAN.md#phase-08` |
| phase_09_selected | 8 | `20_SCHEDULER_ROLLOUT_PLAN.md#phase-09` |

Total affecte : `114/114 jobs`

Reste non affecte : `0`
