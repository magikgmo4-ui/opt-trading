---
doc_id: GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01_IMPLEMENTATION_NOTES
doc_type: implementation_notes
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01
status: draft_for_review
lifecycle_stage: child_implementation_notes
parent_go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01
topic_keys:
  - opt-trading
  - perf
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01/01_IMPLEMENTATION_NOTES.md
point_de_reprise: "Tracer les scripts et references bascules vers les chemins canoniques PERF."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01/00_CADRAGE.md
---

# 01_IMPLEMENTATION_NOTES

## 1_FICHIERS MODIFIES

```text
scripts/desk_pro_ui_toolbox_fix_cmd.sh
scripts/desk_pro_ui_toolbox_final_cmd.sh
modules/simex_bitget_bridge/cmd.sh
scripts/verify_all.sh
modules/desk_pro_orchestrator/app/desk_pro_orchestrator.py
modules/perf/README.md
```

## 2_SWITCH EFFECTIF

```text
FastAPI launch path : perf.perf_app:app -> modules.perf.app:app
Perf engine path    : modules.perf_engine.app.perf_engine -> modules.perf.engine.app.perf_engine

Compat preservee :
- pkill patterns acceptent ancien + nouveau
- anciens modules/shims toujours presents
```

## 3_VALIDATION

```text
- syntaxe shell verifiee
- py_compile nouveaux chemins verifies via verify_all update
- anciens chemins toujours resolvables si rollback necessaire
```
