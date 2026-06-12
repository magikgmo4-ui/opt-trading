---
doc_id: GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01_ROLLBACK_AND_SEQUENCE
doc_type: rollback_sequence
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01
status: draft_for_review
lifecycle_stage: child_rollback_sequence
parent_go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - rollback
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01/03_ROLLBACK_AND_SEQUENCE.md
point_de_reprise: "Definir la sequence de bascule et de rollback PERF."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01/02_SWITCH_GATES.md
---

# 03_ROLLBACK_AND_SEQUENCE

## 1_SWITCH SEQUENCE FUTURE

```text
1. branch de test dediee
2. maj des scripts de lancement et verify_all
3. test import canonique `modules.perf.app:app`
4. test uvicorn local / staging
5. verification /perf/ui + /desk
6. merge seulement si tous les gates passent
```

## 2_ROLLBACK

```text
Rollback = restaurer tous les scripts vers les anciens chemins historiques.
Les shims laissent deja l'ancien et le nouveau coexister, ce qui reduit le risque.
```

## 3_NEXT_GO

```text
GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01
```

## RISKS

- À qualifier.
