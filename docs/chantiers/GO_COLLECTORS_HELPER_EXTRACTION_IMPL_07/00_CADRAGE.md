---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_07_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_07
status: final
lifecycle_stage: closeout
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - helper-extraction
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_07/00_CADRAGE.md
point_de_reprise: "Extraire classify_collector_error commun aux deux collecteurs spot."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_06/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_HELPER_EXTRACTION_IMPL_07

## 1_MASTER_TARGET

Extraire la logique de classification d'erreurs HTTP/provider commune aux deux collecteurs spot dans `collectors_core.lifecycle.classify_collector_error`.

## 2_CHANGEMENTS

```text
collectors_core/lifecycle.py :
  + classify_collector_error (gère ConfigurationError, ValidationError, HttpRequestError)

collectors_core/__init__.py :
  + export classify_collector_error

collector_coingecko/run.py :
  - imports ConfigurationError, HttpRequestError, ValidationError, retry_after_absolute
  + import classify_collector_error
  _classify_error → 1 ligne d'appel

collector_binance_spot/run.py :
  - imports ConfigurationError, HttpRequestError, ValidationError, retry_after_absolute
  - import typing.Any (plus utilisé)
  + import classify_collector_error
  _classify_error → 1 ligne (avec extra_recoverable_codes={418})
```

## RISKS

- À qualifier.
