---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_IMPL_01
doc_type: initial_project_doc
repo: opt-trading
status: closed
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
created_at: 2026-05-17
surface: impl + doc
scope: modules/localcms/app/main.py — _build_metrics() extension
---

# 00_INITIAL_PROJECT_DOC
## GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_IMPL_01

---

## 1_MASTER_TARGET

```text
Implémenter l'extension _build_metrics() définie par PR #525.
Exposer le bloc observation (seuils Phase 1, éligibilité) dans GET /metrics/daily.
Étendre last_run avec session_id, localcms_ok, closeout_required.
```

---

## 2_CONTEXTE_ETABLI

| Fait | Valeur |
| --- | --- |
| `PR #525` | MERGED — spec LocalCMS observation view |
| Option retenue | A — extension `_build_metrics()` uniquement |
| Fichier cible | `modules/localcms/app/main.py` |
| Smoke test | PASS |

---

## 3_SCOPE

- Ajout `from datetime import date` dans les imports
- Ajout constantes `_PHASE1_THRESHOLD_RUNS = 30`, `_PHASE1_THRESHOLD_DAYS = 14`
- Extension `_build_metrics()` — bloc `observation` + extensions `last_run`
- Rétrocompatible — aucun champ existant retiré

## RISKS

- À qualifier.
