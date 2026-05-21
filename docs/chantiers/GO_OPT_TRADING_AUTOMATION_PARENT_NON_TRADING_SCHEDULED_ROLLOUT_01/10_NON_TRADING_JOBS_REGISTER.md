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

## A. Repo / Git / docs

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `repo-status-check` | repo | git | `git status` | read-only | none | none | enabled | 15 min | branch clean report | planned |
| `repo-diff-check` | repo | repo | `git diff --check` | read-only | none | none | enabled | 30 min | whitespace/conflict report | planned |
| `repo-branch-audit` | repo | git | `git branch`/`gh` | read-only | none | none | enabled | daily | merged/orphan branch report | planned |
| `repo-pr-audit` | repo | github | `gh pr list` | read-only | none | none | enabled | hourly | PR state digest | planned |
| `repo-go-index-audit` | repo | docs index | index audit runner | read-only | none | none | enabled | daily | chantier + inbox audit | planned |
| `repo-doc-frontmatter-lint` | repo | docs | frontmatter lint | read-only/report | none | none | enabled | daily | lint report | planned |
| `repo-doc-link-check` | repo | docs | link checker | read-only/report | none | none | enabled | daily | link report | planned |
| `repo-closeout-eligibility-check` | repo | governance docs | closeout audit | read-only | none | none | enabled | daily | closable GO report | planned |
| `repo-parent-coverage-board-refresh` | repo | parent board | board refresh generator | draft only | draft docs only | HITL | manual | manual/HITL | proposed board patch | planned |
| `repo-memory-bricks-candidate-scan` | repo | docs memory | scan runner | read-only/draft | draft docs only | none | enabled | daily | candidate list | planned |
| `repo-changelog-digest` | repo | git/github | changelog digest runner | read-only/report | none | none | enabled | daily | digest report | planned |
| `repo-orphan-files-audit` | repo | repo fs | orphan audit runner | read-only | none | none | enabled | daily | orphan file report | planned |
| `repo-scope-guard` | repo | diff scope | scope guard | read-only | none | none | enabled | pre-commit/manual | out-of-scope report | planned |
| `repo-pr-review-preflight` | repo | PR review | preflight runner | read-only | none | none | manual | manual | preflight checklist | planned |
| `repo-release-note-draft` | repo | docs/release | release note generator | draft only | draft docs only | HITL | manual | manual/HITL | draft note | planned |

## B. Strict workers

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `strict-worker-model-registry-check` | workers | worker registry | `models.registry.json` validator | read-only | none | none | enabled | daily | registry validation PASS | planned |
| `strict-worker-task-index-check` | workers | task index | `tasks.index.json` validator | read-only | none | none | enabled | daily | task index validation PASS | planned |
| `strict-worker-job-packet-validate` | workers | job packets | packet validator | read-only | none | none | on demand | on demand | packet validation report | planned |
| `strict-worker-readonly-smoke` | workers | worker runtime | readonly smoke runner | read-only + reports | reports only | readonly guard | enabled | 6 h | smoke PASS report | planned |
| `strict-worker-output-schema-check` | workers | worker outputs | schema check runner | read-only | none | none | after run | after run | output schema PASS | planned |
| `strict-worker-denied-command-scan` | workers | worker logs | denied command scan | read-only | none | none | after run | after run | no forbidden command report | planned |
| `strict-worker-log-archive` | workers | logs | log archiver | local write logs | local logs only | local-only | enabled | daily | archive artifact | planned |
| `strict-worker-failure-report` | workers | failures | failure reporter | report | reports only | none | on failure | on failure | FAIL/BLOCKED report | planned |

## C. Ledger / observabilite

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `ledger-heartbeat` | ledger | ledger | heartbeat writer | local write ledger | ledger only | local-only | enabled | 15 min | heartbeat event present | planned |
| `ledger-replay-check` | ledger | ledger | replay checker | read-only | none | none | enabled | hourly | replay order PASS | planned |
| `ledger-blocked-events-digest` | ledger | ledger | digest runner | read-only/report | reports only | none | enabled | hourly | BLOCKED/FAIL digest | planned |
| `ledger-rotation-check` | ledger | ledger archive | rotation checker | local write archive | archive only | local-only | enabled | daily | rotation/archive report | planned |
| `ledger-schema-validation` | ledger | ledger | schema validator | read-only | none | none | enabled | hourly | schema PASS | planned |
| `ledger-trace-id-audit` | ledger | ledger | trace audit | read-only | none | none | enabled | daily | trace_id coverage report | planned |
| `automation-health-status` | ledger | local report | status generator | local write report | report only | local-only | enabled | 15 min | `health_status.json` updated | planned |
| `automation-health-digest` | ledger | health summary | digest runner | report | reports only | none | enabled | hourly | health digest | planned |
| `kill-switch-state-check` | ledger | kill switch | state checker | read-only | none | none | enabled | 5 min | kill switch state report | planned |
| `stuck-job-detector` | ledger | scheduler state | stuck job scan | read-only/report | reports only | none | enabled | 15 min | stuck job report | planned |

## D. Securite / secrets / permissions

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `anti-leak-scan` | security | outputs | secret scan | read-only | none | none | enabled | 6 h | no secret report | planned |
| `env-file-presence-check` | security | `.env*` | env audit | read-only | none | none | enabled | daily | env presence report | planned |
| `gitignore-secrets-policy-check` | security | `.gitignore` | policy check | read-only | none | none | enabled | daily | policy PASS | planned |
| `oauth-scope-audit` | security | app scopes | scope audit | read-only/report | reports only | none | enabled | daily | scope drift report | planned |
| `external-token-presence-check` | security | env vars | token presence checker | read-only | none | none | manual/daily | manual/daily | required vars present | planned |
| `permission-drift-check` | security | permissions | drift audit | read-only/report | reports only | none | enabled | daily | drift report | planned |
| `kill-switch-fullstop-test` | security | kill switch | dry-run test | dry-run | none | dry-run guard | manual | manual | controlled test PASS | planned |
| `deny-by-default-check` | security | write gates | policy test | dry-run | none | deny-by-default | enabled | daily | blocked write proof | planned |

## E. HITL / approvals

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `proposal-packet-create` | hitl | proposal | proposal generator | draft | draft packets only | HITL | on demand | on demand | proposal packet | planned |
| `approval-packet-validate` | hitl | approval | approval validator | read-only | none | none | on demand | on demand | approval validity PASS | planned |
| `execution-packet-preflight` | hitl | execution | preflight runner | read-only | none | none | on demand | on demand | preflight PASS | planned |
| `verification-packet-create` | hitl | verification | verification generator | report | reports only | none | after action | after action | verification packet | planned |
| `approval-expiry-check` | hitl | approvals queue | expiry checker | local write status | approval status only | local-only | enabled | hourly | expired approvals updated | planned |
| `dual-confirm-required-check` | hitl | approval policy | dual confirm checker | read-only | none | none | on demand | on demand | dual confirm enforced | planned |
| `hitl-scenarios-smoke` | hitl | HITL flows | scenario smoke runner | dry-run | none | dry-run guard | enabled | nightly | scenario PASS report | planned |
| `pending-approvals-digest` | hitl | approvals queue | digest runner | report | reports only | none | enabled | hourly | pending approvals digest | planned |

## F. Capability matrix / AI team

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `capability-matrix-validate` | ai-team | capability matrix | matrix validator | read-only | none | none | enabled | nightly | matrix PASS | planned |
| `capability-drift-check` | ai-team | app/job mapping | drift checker | read-only/report | reports only | none | enabled | daily | drift report | planned |
| `ai-team-handoff-dry-run` | ai-team | handoff | dry-run | none | dry-run guard | enabled | nightly | handoff PASS report | planned |
| `ai-team-role-registry-check` | ai-team | role registry | registry checker | read-only | none | none | enabled | daily | role registry PASS | planned |
| `handoff-packet-schema-check` | ai-team | handoff packet | schema checker | read-only | none | none | on demand | on demand | schema PASS | planned |
| `memory-broker-dry-run` | ai-team | shared memory | dry-run/local | local memory only | dry-run guard | enabled | nightly | dry-run PASS | planned |
| `task-router-dry-run` | ai-team | task router | dry-run router | dry-run | none | dry-run guard | enabled | nightly | routing PASS | planned |
| `handoff-timeout-check` | ai-team | handoff queue | timeout checker | read-only/report | reports only | none | enabled | hourly | timeout report | planned |

## G. LocalCMS / cockpit

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `localcms-static-cockpit-build` | cockpit | localcms build | static builder | local write build | local build only | local-only | on change | on change | build artifact | planned |
| `localcms-automation-status-sync` | cockpit | localcms status | sync runner | write-gated/local | local rendered views only | local gate | enabled | 30 min | status sync artifact | planned |
| `localcms-workers-state-sync` | cockpit | worker state | sync runner | write-gated/local | local rendered views only | local gate | enabled | 30 min | worker state artifact | planned |
| `localcms-jobs-queue-sync` | cockpit | jobs queue | sync runner | write-gated/local | local rendered views only | local gate | enabled | 30 min | queue artifact | planned |
| `localcms-approvals-sync` | cockpit | approvals | sync runner | write-gated/local | local rendered views only | local gate | enabled | 15 min | approvals artifact | planned |
| `localcms-ledger-view-refresh` | cockpit | ledger view | refresh runner | read/local write view | local rendered views only | local gate | enabled | 15 min | ledger view refreshed | planned |
| `localcms-safe-buttons-check` | cockpit | UI safety | UI checker | read-only | none | none | enabled | daily | safe button report | planned |
| `localcms-kill-switch-widget-check` | cockpit | kill switch widget | UI checker | read-only | none | none | enabled | daily | widget report | planned |

## H. Apps externes

### Airtable

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `airtable-read-health` | app-bridge | airtable | bridge contract | read-only | none | contract | enabled | hourly | read health PASS | planned |
| `airtable-contract-check` | app-bridge | airtable | contract validator | read-only | none | contract | enabled | daily | contract PASS | planned |
| `airtable-canary-proposal` | app-bridge | airtable | proposal runner | draft | draft only | HITL | manual | manual | proposal packet | planned |
| `airtable-canary-write` | app-bridge | airtable | write-gated bridge | write-gated | canary record only | dual confirm | manual puis daily | manual/daily | write + readback proof | planned |
| `airtable-readback-verify` | app-bridge | airtable | verify runner | read-only | none | none | after write | after write | readback PASS | planned |
| `airtable-snapshot-before-write` | app-bridge | airtable | snapshot runner | local/app read | local snapshot only | before write | before write | before write | snapshot captured | planned |
| `airtable-rollback-verify` | app-bridge | airtable | rollback checker | read-only | none | none | after write | after write | rollback feasibility PASS | planned |

### ClickUp

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `clickup-read-health` | app-bridge | clickup | bridge contract | read-only | none | contract | enabled | hourly | read health PASS | planned |
| `clickup-contract-check` | app-bridge | clickup | contract validator | read-only | none | contract | enabled | daily | contract PASS | planned |
| `clickup-canary-proposal` | app-bridge | clickup | proposal runner | draft | draft only | HITL | manual | manual | proposal packet | planned |
| `clickup-canary-task-create` | app-bridge | clickup | write-gated bridge | write-gated | canary task only | dual confirm | manual puis daily | manual/daily | create + readback proof | planned |
| `clickup-task-readback-verify` | app-bridge | clickup | verify runner | read-only | none | none | after write | after write | readback PASS | planned |
| `clickup-task-update-canary` | app-bridge | clickup | write-gated bridge | write-gated | canary field/comment only | dual confirm | manual | manual | update + readback proof | planned |
| `clickup-compensation-note` | app-bridge | clickup | compensation runner | write-gated | compensation note only | HITL | after write | after write | compensation logged | planned |

### Botpress

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `botpress-read-health` | app-bridge | botpress | bridge contract | read-only | none | contract | enabled | hourly | read health PASS | planned |
| `botpress-contract-check` | app-bridge | botpress | contract validator | read-only | none | contract | enabled | daily | contract PASS | planned |
| `botpress-dev-message-proposal` | app-bridge | botpress | proposal runner | draft | draft only | HITL | manual | manual | proposal packet | planned |
| `botpress-dev-message-send` | app-bridge | botpress | write-gated bridge | write-gated | dev test message only | dual confirm | manual | manual | send + readback proof | planned |
| `botpress-variable-update-canary` | app-bridge | botpress | write-gated bridge | write-gated | controlled variable only | dual confirm | manual | manual | update + readback proof | planned |
| `botpress-readback-verify` | app-bridge | botpress | verify runner | read-only | none | none | after write | after write | readback PASS | planned |

### KG Repo

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `kg-repo-read-index` | app-bridge | repo kg | kg reader | read-only | none | none | enabled | hourly/daily | index read PASS | planned |
| `kg-repo-drift-check` | app-bridge | repo kg | drift checker | read-only | none | none | enabled | daily | drift report | planned |
| `kg-repo-node-proposal` | app-bridge | repo kg | proposal runner | draft | draft only | HITL | enabled | daily | proposal packet | planned |
| `kg-repo-pr-gated-sync` | app-bridge | repo kg | PR workflow | PR-gated | PR only | PR review | manual | manual | merged PR proof | planned |
| `kg-repo-readback-verify` | app-bridge | repo kg | verify runner | read-only | none | none | after PR | after PR | readback PASS | planned |
| `kg-repo-orphan-node-audit` | app-bridge | repo kg | orphan audit | read-only/report | reports only | none | enabled | daily | orphan node report | planned |

### Google Sheets

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `sheets-read-health` | app-bridge | google sheets | bridge contract | read-only | none | contract | enabled | hourly | read health PASS | planned |
| `sheets-report-export-proposal` | app-bridge | google sheets | proposal runner | draft | draft only | HITL | manual | manual | proposal packet | planned |
| `sheets-canary-cell-write` | app-bridge | google sheets | write-gated bridge | write-gated | canary range only | dual confirm | manual | manual | write + readback proof | planned |
| `sheets-readback-verify` | app-bridge | google sheets | verify runner | read-only | none | none | after write | after write | readback PASS | planned |
| `sheets-snapshot-before-write` | app-bridge | google sheets | snapshot runner | read-only/local | local snapshot only | before write | before write | before write | snapshot captured | planned |

### Telegram non-trading

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `telegram-notification-health` | app-bridge | telegram | notifier | write notification | notification only | notification policy | manual/daily | manual/daily | delivery proof | planned |
| `telegram-automation-digest` | app-bridge | telegram | digest sender | notification only | notification only | notification policy | enabled | daily | digest delivered | planned |
| `telegram-blocked-events-alert` | app-bridge | telegram | alert sender | notification only | notification only | alert policy | on failure | on failure | alert delivered | planned |
| `telegram-approval-reminder` | app-bridge | telegram | reminder sender | notification only | notification only | notification policy | enabled | hourly | reminder delivered | planned |

### Gmail / Calendar / Drive

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `gmail-read-report-inbox` | app-bridge | gmail | bridge contract | read-only | none | contract | enabled | daily | read PASS | planned |
| `gmail-draft-report` | app-bridge | gmail | draft generator | write-gated/draft | draft only | HITL | manual | manual | draft created | planned |
| `calendar-read-automation-events` | app-bridge | calendar | bridge contract | read-only | none | contract | enabled | daily | read PASS | planned |
| `calendar-create-review-event` | app-bridge | calendar | write-gated bridge | write-gated | review event only | dual confirm | manual | manual | event created | planned |
| `drive-read-folder-health` | app-bridge | drive | bridge contract | read-only | none | contract | enabled | daily | read PASS | planned |
| `drive-upload-report-canary` | app-bridge | drive | write-gated bridge | write-gated | canary upload only | dual confirm | manual | manual | upload proof | planned |

## I. Scheduler / CI

| job_id | category | surface | script_or_tool | mode | allowed_writes | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `scheduler-config-validate` | scheduler | scheduler config | config validator | read-only | none | none | on change | on change | config PASS | planned |
| `scheduler-unit-lint` | scheduler | `.service/.timer` | unit lint | read-only | none | none | on change | on change | unit lint PASS | planned |
| `scheduler-user-timers-list` | scheduler | timers | timers list runner | read-only | none | none | enabled | hourly | timers inventory | planned |
| `scheduler-dry-run-next-fire` | scheduler | timer schedule | next-fire calculator | read-only | none | none | enabled | daily | next fire report | planned |
| `scheduler-dead-letter-check` | scheduler | dead-letter queue | queue reader | read-only | none | none | enabled | hourly | dead-letter report | planned |
| `scheduler-retry-policy-check` | scheduler | retry policy | policy validator | read-only | none | none | enabled | daily | retry policy PASS | planned |
| `ci-nightly-validation` | scheduler | CI | validation workflow | CI/local | CI artifacts only | CI policy | enabled | nightly | CI PASS | planned |
| `ci-status-ingest` | scheduler | CI status | ingest runner | write-gated/local | local status only | local gate | enabled | hourly | status ingest artifact | planned |

## Priorisation pour utilisation reelle

### Phase 01 - immediat

```text
repo-status-check
repo-diff-check
repo-pr-audit
automation-health-status
ledger-heartbeat
ledger-replay-check
anti-leak-scan
strict-worker-readonly-smoke
capability-matrix-validate
ai-team-handoff-dry-run
bridge-contract-validation
hitl-scenarios-smoke
localcms-automation-status-sync
```

### Phase 02 - apps externes canary

```text
clickup-canary-task-create
airtable-canary-write
botpress-dev-message-send
kg-repo-node-proposal / pr-gated-sync
localcms-status-sync
telegram-automation-digest
```

### Phase 03 - scheduler reel

```text
scheduler-user-timers-list
automation-health-status.timer
automation-ledger-heartbeat.timer
automation-nightly-validation.timer
external-apps-canary.timer
```
