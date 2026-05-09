---
doc_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01_TARGET_SHAPE
doc_type: target_shape
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01
status: draft_for_review
lifecycle_stage: child_target_shape
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01
topic_keys:
  - opt-trading
  - perf
  - target-shape
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01/01_TARGET_SHAPE.md
point_de_reprise: "Fixer la forme cible potentielle du cluster PERF."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01/00_CADRAGE.md
---

# 01_TARGET_SHAPE

## 1_FORME CIBLE PROPOSEE

```text
modules/perf/
├── README.md
├── __init__.py
├── app.py            ← ex-perf/perf_app.py
├── engine/           ← ex-modules/perf_engine/
├── webhook.py        ← ex-adapters/webhook_to_perf.py
├── scripts/          ← facade shell maintenue
└── data/             ← emplacement cible futur de perf.db
```

## 2_PRINCIPES

```text
- conserver une facade operateur stable
- rapprocher code runtime et code famille
- isoler la DB dans un emplacement explicite
- ne pas casser desk_pro mount
- garder webhook_to_perf visible dans la famille PERF
```

## 3_DECISION GATE

```text
La forme cible n'est qu'une hypothese de travail.
Elle n'est executable qu'apres analyse complete des impacts et rollback.
```
