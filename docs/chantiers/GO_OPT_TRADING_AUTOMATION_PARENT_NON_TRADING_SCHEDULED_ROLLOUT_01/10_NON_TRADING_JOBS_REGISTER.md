---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_NON_TRADING_JOBS_REGISTER
doc_type: jobs_register
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: draft
---

# 10_NON_TRADING_JOBS_REGISTER

## Schema canonique

Colonnes attendues:

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

## Categories couvertes

- Repo / Git / docs
- Strict workers
- Ledger / observabilite
- Securite / secrets / permissions
- HITL / approvals
- Capability matrix / AI team
- LocalCMS / cockpit
- Apps externes
- Scheduler / CI

## Phase 01 shortlist

| job_id | category | surface | mode | gate | scheduler | frequency | evidence_required | status |
|---|---|---|---|---|---|---|---|---|
| `repo-status-check` | repo | git | read-only | none | enabled | 15 min | status report clean | proposed |
| `repo-diff-check` | repo | repo | read-only | none | enabled | 30 min | `git diff --check` PASS | proposed |
| `repo-pr-audit` | repo | github | read-only | none | enabled | hourly | PR digest | proposed |
| `automation-health-status` | ledger | local report | local write report | local-only | enabled | 15 min | `health_status.json` updated | proposed |
| `ledger-heartbeat` | ledger | ledger | local write ledger | local-only | enabled | 15 min | heartbeat event present | proposed |
| `ledger-replay-check` | ledger | ledger | read-only | none | enabled | hourly | replay order PASS | proposed |
| `anti-leak-scan` | security | outputs | read-only | none | enabled | 6 h | no secrets found | proposed |
| `strict-worker-readonly-smoke` | workers | worker runtime | read-only + reports | readonly guard | enabled | 6 h | smoke report PASS | proposed |
| `capability-matrix-validate` | ai-team | matrix docs | read-only | none | enabled | nightly | matrix validation PASS | proposed |
| `ai-team-handoff-dry-run` | ai-team | handoff | dry-run | dry-run guard | enabled | nightly | handoff dry-run PASS | proposed |
| `bridge-contract-validation` | apps | bridges | read-only | contract gate | enabled | daily | contract validation PASS | proposed |
| `hitl-scenarios-smoke` | hitl | approvals | dry-run | HITL gate | enabled | nightly | scenarios PASS | proposed |
| `localcms-automation-status-sync` | cockpit | localcms | write-gated/local | local gate | enabled | 30 min | sync artifact rendered | proposed |

## Source brute

La liste maitre complete reste capturee dans `GO_CANVAS.md` et doit etre
normalisee ici lors de la prochaine passe.
