---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_03_IMPLEMENTATION_NOTES
doc_type: implementation_notes
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_03
status: draft_for_review
lifecycle_stage: child_implementation_notes
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_03/01_IMPLEMENTATION_NOTES.md
point_de_reprise: "Tracer les builders status centralisés dans collectors_core.lifecycle."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_03/00_CADRAGE.md
---

# 01_IMPLEMENTATION_NOTES

## 1_NOUVEAUX HELPERS PARTAGES

```text
collectors_core.lifecycle
  - safe_previous_status
  - build_running_status
  - build_success_status
  - build_failure_status
```

## 2_MODULES CONSOMMATEURS

```text
- collector_coingecko.run
- collector_binance_spot.run
```

## 3_BENEFICE

```text
Moins de duplication spot lifecycle.
Doctrines status/freshness alignées par construction.
```
