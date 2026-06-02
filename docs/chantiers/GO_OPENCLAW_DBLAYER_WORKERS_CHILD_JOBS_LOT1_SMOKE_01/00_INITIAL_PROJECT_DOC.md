---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_SMOKE_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_SMOKE_01
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: open
opened_at: 2026-06-01
---

# GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_SMOKE_01

## 1_MASTER_TARGET

Valider en run réel les 15 jobs Lot 1 identifiés dans
`GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_ACTIVATION_PRIORITY_01`.
Chaque job doit s'exécuter sans erreur fatale et produire une sortie
cohérente (exit 0 ou rapport valide).

## 2_CONTEXT

Lot 1 = 14 jobs `script_direct` + 1 job `dispatcher`.
Tous ont un script Python dans `scripts/ai/workers/` ou un packet validé.
Tous ont un PASS dans les phases 01–03 du parent rollout.

## 3_JOBS COUVERTS

| # | job_id | script |
|---|---|---|
| 1 | automation-health-status | health_status.py |
| 2 | ledger-heartbeat | ledger_writer.py |
| 3 | stuck-job-detector | stuck_job_detector.py |
| 4 | ledger-replay-check | ledger_replay.py |
| 5 | ledger-schema-validation | ledger_schema_validation.py |
| 6 | ledger-blocked-events-digest | ledger_blocked_events_digest.py |
| 7 | localcms-automation-status-sync | localcms_automation_status_sync.py |
| 8 | strict-worker-readonly-smoke | dispatcher → GO_STRICT_WORKERS_READONLY_SMOKE_01 |
| 9 | strict-worker-log-archive | strict_worker_log_archive.py |
| 10 | strict-worker-denied-command-scan | strict_worker_denied_command_scan.py |
| 11 | permission-drift-check | permission_drift_check.py |
| 12 | repo-doc-frontmatter-lint | repo_doc_frontmatter_lint.py |
| 13 | repo-doc-link-check | repo_doc_link_check.py |
| 14 | ledger-rotation-check | ledger_rotation_check.py |
| 15 | repo-pr-audit | gh pr list |

## 4_SUCCESS_CRITERIA

```
✓ 15/15 jobs lancés
✓ Exit 0 ou rapport valide pour chaque job
✓ Aucune écriture non-locale (pas de push, pas de write externe)
✓ Résultats consignés dans 10_SMOKE_RESULTS.md
```
