---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_09_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_09
status: final
lifecycle_stage: closeout
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - helper-extraction
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_09/00_CADRAGE.md
point_de_reprise: "Centraliser ErrorInfo dans collectors_core.lifecycle."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_08/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_HELPER_EXTRACTION_IMPL_09

## 1_MASTER_TARGET

Centraliser la dataclass `ErrorInfo` (identiques dans les deux collecteurs spot) dans `collectors_core.lifecycle`.

## 2_CHANGEMENTS

```text
collectors_core/lifecycle.py :
  + ErrorInfo dataclass
  + classify_collector_error retourne ErrorInfo directement (plus de dict)

collectors_core/__init__.py :
  + export ErrorInfo

collector_coingecko/run.py :
  - local ErrorInfo
  - from dataclasses import dataclass
  + import ErrorInfo from collectors_core
  _classify_error → 1 ligne

collector_binance_spot/run.py :
  - local ErrorInfo
  - from dataclasses import dataclass
  + import ErrorInfo from collectors_core
  _classify_error → 1 ligne
```

## RISKS

- À qualifier.
