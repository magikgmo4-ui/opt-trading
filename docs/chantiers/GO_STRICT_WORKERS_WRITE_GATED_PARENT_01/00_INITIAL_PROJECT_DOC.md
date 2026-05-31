---
doc_id: GO_STRICT_WORKERS_WRITE_GATED_PARENT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_STRICT_WORKERS_WRITE_GATED_PARENT_01
parent_go: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: closed
lifecycle_stage: closed
created_at: 2026-05-31
task_type: PARENT
autonomy_max: N/A
---

# 00_INITIAL_PROJECT_DOC — GO_STRICT_WORKERS_WRITE_GATED_PARENT_01

## 1_MASTER_TARGET

Prouver le cadre WRITE_GATED du strict workers framework :
- créer `runner_writegated.py` (runner contrôlé avec gate d'approbation explicite) ;
- exécuter un smoke test end-to-end : dry-run + gate APPROVE + write réel sur cible autorisée ;
- documenter la chaîne complète : read → write_plan → dry-run → gate → write.

## 2_PRECONDITIONS

```text
runner_readonly.py      = PASS (GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01, PR #995)
PATCH_DRAFT cycle       = PASS (PR #1021 + PR #1022)
tasks.index.json        = WRITE_GATED entry présente (A4, write_allowlist défini)
write_allowlist targets = reports/ai/workers/*.md, scripts/ai/workers/job_packets/*.json
```

## 3_GAPS

| Gap | GO dédié | Statut |
| --- | --- | --- |
| runner_writegated.py + smoke | GO_STRICT_WORKERS_CHILD_RUNNER_WRITEGATED_01 | open |

## 4_CRITERES_PASS

| Critère | Requis |
| --- | --- |
| runner_writegated.py opérationnel | PASS |
| dry-run : DRY_RUN_PASS, 0 writes | oui |
| real run + --gate-approved : write réel sur cible autorisée | oui |
| target hors allowlist : BLOCKED | oui |
| git status post-run : cible dans allowlist créée | oui |

## 12_INVARIANTS

```text
- Writes bloqués sans --gate-approved
- Cibles limitées à write_allowlist
- forbidden_targets respectés (tasks.index.json, models.registry.json, etc.)
- Gate documenté avant chaque write
```
