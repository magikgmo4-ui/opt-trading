---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10_V2_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10_V2
status: final
lifecycle_stage: closeout
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - final-cleanup
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10_V2/00_CADRAGE.md
point_de_reprise: "Nettoyage final : inline _classify_error dans les deux collecteurs spot."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_09/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10_V2

## 1_MASTER_TARGET

Nettoyage final de la chaîne COLLECTORS : inline `_classify_error` (déjà 1 ligne) directement dans `run_collection`.

## 2_CHANGEMENTS

```text
collector_coingecko/run.py :
  - _classify_error retiré
  + classify_collector_error(exc) appelé directement

collector_binance_spot/run.py :
  - _classify_error retiré
  + classify_collector_error(exc, extra_recoverable_codes={418}) appelé directement
```

## RISKS

- À qualifier.
