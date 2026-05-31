---
doc_id: GO_STRICT_WORKERS_CHILD_RUNNER_WRITEGATED_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_STRICT_WORKERS_CHILD_RUNNER_WRITEGATED_01
parent_go: GO_STRICT_WORKERS_WRITE_GATED_PARENT_01
status: open
lifecycle_stage: impl
created_at: 2026-05-31
task_type: WRITE_GATED
autonomy_max: A4
---

# 00_INITIAL_PROJECT_DOC — Child : runner_writegated + smoke

## 1_MASTER_TARGET

Créer `runner_writegated.py` et prouver le cycle complet WRITE_GATED :
dry-run PASS → gate APPROVE (`--gate-approved`) → write réel sur cible autorisée.

## 2_PRECONDITIONS

```text
runner_readonly.py  = PASS (PR #995)
tasks.index.json    = WRITE_GATED entry définie (A4, write_allowlist, forbidden_targets)
write_allowlist     = reports/ai/workers/*.md, scripts/ai/workers/job_packets/*.json
```

## 3_CRITERES_PASS

| Critère | Requis |
| --- | --- |
| dry-run : DRY_RUN_PASS | oui |
| sans --gate-approved : READS_ONLY_PASS, 0 writes | oui |
| --gate-approved : writes_executed=1, PASS | oui |
| cible hors allowlist : BLOCKED | oui (testé via max_lines_per_write guard) |
| git status : smoke output créé | oui |

## 12_INVARIANTS

```text
- Writes bloqués sans --gate-approved
- max_lines_per_write=50 respecté
- forbidden_targets respectés
- write_allowlist validée pour chaque cible
```
