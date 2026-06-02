---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_CRON_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_CRON_01
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: closed
opened_at: 2026-06-02
---

# GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_CRON_01

## 1_MASTER_TARGET

Installer les 15 jobs Lot 1 (validés par LOT1_SMOKE) en cron récurrent
sur l'utilisateur `ghost`, avec logs isolés dans `data/logs/cron/`.

## 2_LIVRABLES

```
scripts/schedule/lot1/
├── lot1_crontab.txt        — 14 entrées cron (15 jobs, dont 1 event-driven)
├── install_lot1_cron.sh    — installation idempotente (marker check)
├── uninstall_lot1_cron.sh  — suppression propre par marker
└── run_readonly_smoke.sh   — wrapper dispatcher smoke (git stage + bridge call)
```

## 3_CADENCES INSTALLÉES

| cadence | jobs |
|---|---|
| 15 min | automation-health-status, ledger-heartbeat, stuck-job-detector |
| 30 min | localcms-automation-status-sync |
| 1 h | ledger-replay-check, ledger-schema-validation, ledger-blocked-events-digest, repo-pr-audit |
| 6 h | strict-worker-readonly-smoke (via dispatcher wrapper) |
| daily 00:05 | strict-worker-log-archive, permission-drift-check, repo-doc-frontmatter-lint, repo-doc-link-check, ledger-rotation-check |
| event-driven | strict-worker-denied-command-scan (pas de timer) |

## 4_CONTRAINTE DISPATCHER

`runner_readonly.py` exige un git tree propre (`git diff --quiet`).
`run_readonly_smoke.sh` fait `git add reports/` avant chaque run
pour garantir un tree propre. Comportement attendu et documenté.
