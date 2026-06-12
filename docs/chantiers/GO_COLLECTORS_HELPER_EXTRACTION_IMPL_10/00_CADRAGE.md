---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10
status: final
lifecycle_stage: closeout
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - final-cleanup
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10/00_CADRAGE.md
point_de_reprise: "Nettoyage final : inline _classify_error, fix doublon Binance."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_09/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10

## 1_MASTER_TARGET

Nettoyage final de la chaîne COLLECTORS : inline le dernier wrapper trivial `_classify_error` et corriger un doublon accidentel dans `collector_binance_spot`.

## 2_CHANGEMENTS

```text
collector_coingecko/run.py :
  - _classify_error retiré
  + classify_collector_error appelé directement dans run_collection

collector_binance_spot/run.py :
  - _classify_error retiré
  - doublon run_collection corrigé
  + classify_collector_error appelé directement dans run_collection
```

## 3_FONCTIONS LOCALES RESTANTES

```text
Coingecko (4) : run_sanity, run_collection, read_status, status_as_text, _build_manifest, _build_latest
Binance  (5) : run_sanity, run_collection, read_status, status_as_text, _build_manifest, _build_latest

Toutes sont soit public API (read_status, status_as_text), soit des builders provider-specific necessaires.
La chaîne COLLECTORS helper extraction est close.
```

## RISKS

- À qualifier.
