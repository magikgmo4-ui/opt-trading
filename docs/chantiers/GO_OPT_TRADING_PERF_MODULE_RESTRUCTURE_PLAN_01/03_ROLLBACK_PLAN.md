---
doc_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01_ROLLBACK_PLAN
doc_type: rollback_plan
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01
status: draft_for_review
lifecycle_stage: child_rollback_plan
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01
topic_keys:
  - opt-trading
  - perf
  - rollback
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01/03_ROLLBACK_PLAN.md
point_de_reprise: "Definir le rollback minimal avant toute implementation PERF."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01/02_IMPACT_ANALYSIS.md
---

# 03_ROLLBACK_PLAN

## 1_PRECONDITIONS

```text
Avant toute implementation future :
- backup du fichier perf/perf_app.py
- backup du repertoire modules/perf_engine/
- backup de adapters/webhook_to_perf.py
- backup de perf/perf.db
- backup des scripts shell et unit files lies a PERF
```

## 2_ROLLBACK MINIMAL

```text
- restaurer anciens chemins de fichiers
- restaurer ancien uvicorn module path
- restaurer ancien chemin SQLite
- restaurer anciens wrappers shell
- verifier /perf/ui et /desk montent de nouveau
```

## 3_NEXT_GO

```text
GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01
```
