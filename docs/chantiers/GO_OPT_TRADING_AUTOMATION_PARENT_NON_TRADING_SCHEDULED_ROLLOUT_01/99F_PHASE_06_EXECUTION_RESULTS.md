---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_PHASE_06_EXECUTION_RESULTS
doc_type: execution_results
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: active
---

# 99F_PHASE_06_EXECUTION_RESULTS

## Verdict: `PHASE_06_EXECUTED`

## Count: `7 jobs`

## Execution breakdown

| job_id | status | detail |
|---|---|---|
| `localcms-static-cockpit-build` | WARN | FastAPI module not importable in current venv (expected — localcms designed for FastAPI serving); 1196 LOC cockpit module present with HTML/journal/metrics UI |
| `localcms-workers-state-sync` | PASS | 23 worker reports, tasks.index.json, models.registry.json, archive all present |
| `localcms-jobs-queue-sync` | PASS | 4 scheduler jobs, 1 alert, 1 dead letter, 22 job packets available |
| `localcms-approvals-sync` | PASS | 2 proposals (1 pending, 1 executed), 1 verification packet |
| `localcms-ledger-view-refresh` | PASS | overall PASS, 1034 healthcheck entries, 446KB, kill switch NORMAL, 12/12 blocks PASS |
| `localcms-safe-buttons-check` | PASS | 13 GET endpoints, 0 write endpoints — no dangerous UI buttons |
| `localcms-kill-switch-widget-check` | WARN | Kill switch state NORMAL, dir exists but not referenced in LocalCMS UI code |

## Results summary

| category | count |
|---|---|
| PASS | 5 |
| WARN | 2 |
| FAIL | 0 |

## Non-blocking findings

1. **FastAPI not in current venv** — cosmetic; localcms is designed for `uvicorn modules.localcms.app.main:app`
2. **Kill switch widget missing from LocalCMS UI** — kill switch state is readable but not exposed in the cockpit HTML

## Gate recommendation

**Gate: PASS_WITH_FINDINGS**
