---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_05_IMPLEMENTATION_NOTES
doc_type: implementation_notes
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_05
status: draft_for_review
lifecycle_stage: child_implementation_notes
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_05/01_IMPLEMENTATION_NOTES.md
point_de_reprise: "Tracer les helpers status/runtime-dir centralisés."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_05/00_CADRAGE.md
---

# 01_IMPLEMENTATION_NOTES

## 1_NOUVEAUX HELPERS PARTAGES

```text
collectors_core.files
  - ensure_writable_directories

collectors_core.lifecycle
  - read_status_payload
  - status_payload_as_text
```

## 2_MODULES CONSOMMATEURS

```text
- collector_coingecko.run
- collector_binance_spot.run
```

## 3_BENEFICE

```text
Le socle runtime/lifecycle spot devient encore plus homogène,
sans aucune modification du métier ni des providers.
```
