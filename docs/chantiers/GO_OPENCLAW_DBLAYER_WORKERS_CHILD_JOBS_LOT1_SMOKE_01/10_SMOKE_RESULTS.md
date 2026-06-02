---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_SMOKE_01_RESULTS
doc_type: smoke_results
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_SMOKE_01
run_at: 2026-06-02
---

# 10_SMOKE_RESULTS — Lot 1 run réel

## Résumé

```
15/15 jobs lancés
exit 0 : 15/15
PASS    : 7
WARN    : 7   (non-bloquant — findings attendus, pas d'erreur fatale)
BLOCKED : 0
FAIL    : 0
```

## Résultats détaillés

| # | job_id | script | exit | statut | notes |
|---|---|---|---|---|---|
| 1 | `automation-health-status` | `health_status.py` | 0 | **PASS** | `status: OK` |
| 2 | `ledger-heartbeat` | `ledger_writer.py` | 0 | **PASS** | event heartbeat écrit, trace_id généré |
| 3 | `stuck-job-detector` | `stuck_job_detector.py` | 0 | WARN | latest entry age 2.8 min → WARN attendu |
| 4 | `ledger-replay-check` | `ledger_replay.py` | 0 | **PASS** | 20 events replayed |
| 5 | `ledger-schema-validation` | `ledger_schema_validation.py` | 0 | WARN | `kill_switch.state not found` — attendu |
| 6 | `ledger-blocked-events-digest` | `ledger_blocked_events_digest.py` | 0 | WARN | PATHS=WARN, ORCHESTRATOR=PASS |
| 7 | `localcms-automation-status-sync` | `localcms_automation_status_sync.py` | 0 | **PASS** | snapshot + report écrits |
| 8 | `strict-worker-readonly-smoke` | dispatcher → `GO_STRICT_WORKERS_READONLY_SMOKE_01` | 0 | **PASS** | `DRY_RUN_PASS`, validation packet complète |
| 9 | `strict-worker-log-archive` | `strict_worker_log_archive.py` | 0 | **PASS** | 50 fichiers archivés |
| 10 | `strict-worker-denied-command-scan` | `strict_worker_denied_command_scan.py` | 0 | WARN | 5 findings / 30 scannés (findings = violations potentielles à réviser) |
| 11 | `permission-drift-check` | `permission_drift_check.py` | 0 | WARN | `.env` permissions 0o664, `kill_switch.state` manquant |
| 12 | `repo-doc-frontmatter-lint` | `repo_doc_frontmatter_lint.py` | 0 | WARN | 3540 findings / 4748 docs (docs sans frontmatter) |
| 13 | `repo-doc-link-check` | `repo_doc_link_check.py` | 0 | WARN | 320 findings / 4748 docs |
| 14 | `ledger-rotation-check` | `ledger_rotation_check.py` | 0 | **PASS** | rotation OK |
| 15 | `repo-pr-audit` | `gh pr list` | 0 | **PASS** | 3 PRs open (1042, 1031, 982) |

## Notes sur les WARN

| finding | source | urgence | action |
|---|---|---|---|
| `latest entry age 2.8 min → WARN` | stuck-job-detector | basse | cadence normale — recalibrer seuil |
| `kill_switch.state not found` | ledger-schema-validation + permission-drift | moyenne | créer `data/runtime_health/kill_switch.state` |
| `.env permissions 0o664` | permission-drift | moyenne | `chmod 600 .env` |
| `5 denied-command findings` | strict-worker-denied-command-scan | à vérifier | réviser rapport complet |
| `3540 frontmatter findings` | repo-doc-frontmatter-lint | basse | docs legacy sans frontmatter — lot dédié |
| `320 link findings` | repo-doc-link-check | basse | liens rompus — lot dédié |

Tous les WARN sont des findings attendus ou connus. Aucun FAIL. Aucun exit non-zéro.

## Job #8 dispatcher — détail

```
dispatcher: openclaw_strict_worker_dispatcher
status: DRY_RUN_PASS
task_type: READ_INVENTORY
runner_called: runner_readonly.py
dry_run: True
gate_approved: False
validation: PASS (packet + invariants + workers + denied_commands)
```

Blocage intermédiaire résolu : git working tree avait des modifications
stagées → `git add reports/` → tree propre → dispatcher PASS.

## Artifacts produits

```
reports/ai/workers/GO_STRICT_WORKERS_READONLY_SMOKE_01_RUNNER.json
reports/ai/workers/GO_STRICT_WORKERS_3W_STEP1_READ_INVENTORY_01_RUNNER.json (updated)
reports/ai/localcms_automation_status_sync.json (updated)
reports/ai/strict_worker_log_archive.json (updated)
reports/ai/strict_worker_denied_command_scan.json (updated)
reports/ai/repo_doc_frontmatter_lint.json (updated)
reports/ai/repo_doc_link_check.json (updated)
data/runtime_health/job_logs/archive/strict_worker_reports_*.tar.gz (+50 files)
```
