---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_06_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_06
status: final
lifecycle_stage: closeout
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - helper-extraction
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_06/00_CADRAGE.md
point_de_reprise: "Remplacer _ensure_errors_artifact par ensure_file dans binance spot."
updated_at: 2026-05-11
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_05/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_HELPER_EXTRACTION_IMPL_06

## 1_MASTER_TARGET

Remplacer la fonction locale `_ensure_errors_artifact` du collecteur Binance Spot par `ensure_file` déjà fourni par `collectors_core.files`.

## 2_CHANGEMENT

```text
collector_binance_spot/run.py :
  + import ensure_file
  - _ensure_errors_artifact function
  - appel remplacé par ensure_file(config.paths.errors_path)
```

## 12_INVARIANTS

```text
- aucun changement métier
- aucun changement runtime
- collector_coingecko non touché
```
