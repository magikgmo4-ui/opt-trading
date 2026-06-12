---
doc_id: GO_OPT_TRADING_PERF_DB_PATH_SWITCH_IMPL_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_PATH_SWITCH_IMPL_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - db
  - path-switch
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_PATH_SWITCH_IMPL_01/00_CADRAGE.md
point_de_reprise: "Basculer les launchers PERF vers le chemin DB canonique s'il existe, sinon fallback legacy."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01/90_CLOSEOUT.md
---

# 00_CADRAGE — PERF_DB_PATH_SWITCH_IMPL_01

## 1_MASTER_TARGET

Implémenter un basculement non cassant des launchers PERF vers le chemin DB canonique, avec fallback automatique legacy.

## 2_STRATEGY

```text
priority:
1. PERF_DB_PATH explicite
2. modules/perf/data/perf.db si present
3. perf/perf.db sinon
```

## RISKS

- À qualifier.
