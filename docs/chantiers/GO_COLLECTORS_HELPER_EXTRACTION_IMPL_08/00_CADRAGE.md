---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_08_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_08
status: final
lifecycle_stage: closeout
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - helper-extraction
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_08/00_CADRAGE.md
point_de_reprise: "Inline _ensure_runtime_directories dans les deux collecteurs spot."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_07/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_HELPER_EXTRACTION_IMPL_08

## 1_MASTER_TARGET

Nettoyer les derniers wrappers fins restants dans les collecteurs spot en inlinant `_ensure_runtime_directories`.

## 2_CHANGEMENTS

```text
collector_coingecko/run.py :
  - _ensure_runtime_directories retiré
  + appel ensure_writable_directories(...) inliné dans run_sanity et run_collection

collector_binance_spot/run.py :
  - _ensure_runtime_directories retiré
  + appel ensure_writable_directories(...) inliné dans run_sanity et run_collection
```

## RISKS

- À qualifier.
