---
doc_id: GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01
topic_keys:
  - opt-trading
  - perf
  - path-switch
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01/00_CADRAGE.md
point_de_reprise: "Basculer les scripts PERF vers les chemins canoniques sans retirer la compat historique."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01/90_CLOSEOUT.md
---

# 00_CADRAGE — PERF_PATH_SWITCH_IMPL_01

## 1_MASTER_TARGET

Basculer les scripts et références opérationnelles PERF vers `modules.perf.*`, en conservant les anciens chemins comme fallback de compatibilité.

## 2_IMPLÉMENTATION RETENUE

```text
- uvicorn launch scripts -> modules.perf.app:app
- subprocess perf engine registry -> modules.perf.engine.app.perf_engine
- verify_all compile -> ajoute les chemins canoniques
- anciens chemins non supprimés
```
