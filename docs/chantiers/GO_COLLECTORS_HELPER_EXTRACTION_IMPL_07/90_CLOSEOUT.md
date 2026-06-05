---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_07_CLOSEOUT
doc_type: closeout
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
  - closeout
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_07/90_CLOSEOUT.md
point_de_reprise: "7e lot helper extraction livré. Dernière grosse duplication spot éliminée."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_07/00_CADRAGE.md
---

# 90_CLOSEOUT — GO_COLLECTORS_HELPER_EXTRACTION_IMPL_07

## 1_VERDICT

```text
VERDICT = PASS
```

## 2_RESULTAT

```text
collectors_core.lifecycle.classify_collector_error centralise la logique
de classification d'erreurs (ConfigurationError, ValidationError, HttpRequestError).

collector_coingecko et collector_binance_spot :
  - 4 imports chacun en moins
  - _classify_error réduit à 1 appel simple
  - argument extra_recoverable_codes pour le status 418 spécifique Binance

py_compile PASS
import des deux classify_error PASS
```

## 3_NEXT_GO

```text
GO_COLLECTORS_HELPER_EXTRACTION_IMPL_08
```

## RISKS

- À qualifier.
