---
doc_id: GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - path-switch
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01/00_CADRAGE.md
point_de_reprise: "Planifier le basculement optionnel des scripts PERF vers les chemins canoniques."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01

## 1_MASTER_TARGET

Planifier le basculement optionnel des scripts et références PERF vers les nouveaux chemins canoniques `modules.perf.*`, sans exécuter ce basculement dans ce GO.

## 12_INVARIANTS

```text
- docs only
- 0 path switch execute
- 0 changement uvicorn effectif
- 0 changement SQLite path effectif
```
