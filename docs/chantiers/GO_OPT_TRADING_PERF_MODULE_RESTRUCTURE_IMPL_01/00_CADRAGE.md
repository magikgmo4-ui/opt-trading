---
doc_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01
topic_keys:
  - opt-trading
  - perf
  - restructure
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01/00_CADRAGE.md
point_de_reprise: "Implementer la structure PERF canonique sans casser les anciens chemins runtime."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01/90_CLOSEOUT.md
---

# 00_CADRAGE — PERF_MODULE_RESTRUCTURE_IMPL_01

## 1_MASTER_TARGET

Implementer une structure canonique `modules/perf/` par shims compatibles, sans casser `perf/perf_app.py`, `modules/perf_engine/` ni `adapters/webhook_to_perf.py`.

## 2_CHOIX D'IMPLEMENTATION

```text
Implementation retenue :
- creer la structure canonique sous modules/perf/
- conserver tous les anciens chemins historiques
- exposer les nouveaux chemins par wrappers Python minces
- ne pas deplacer la DB ni changer uvicorn dans ce lot
```

## 12_INVARIANTS

```text
- compatibilite d'abord
- 0 changement uvicorn
- 0 changement SQLite path
- 0 suppression des anciens chemins
- 0 secret
```
