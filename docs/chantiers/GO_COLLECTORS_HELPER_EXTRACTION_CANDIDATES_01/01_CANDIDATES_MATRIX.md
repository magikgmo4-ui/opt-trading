---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01_CANDIDATES_MATRIX
doc_type: candidates_matrix
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
status: draft_for_review
lifecycle_stage: child_candidates_matrix
parent_go_id: GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01
topic_keys:
  - opt-trading
  - collectors
  - helper-extraction
  - matrix
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01/01_CANDIDATES_MATRIX.md
point_de_reprise: "Matrice des helpers potentiellement extractibles."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01/00_CADRAGE.md
---

# 01_CANDIDATES_MATRIX

## 1_EXTRACTION CANDIDATES

| Zone | Candidate | Extractible ? | Pourquoi |
|---|---|---|---|
| lifecycle | manifest/status/latest writers | OUI | vocabulaire famille déjà gelé |
| logging | events/errors append-only helpers | OUI | enveloppe générique |
| config | layer-order resolution helpers | OUI | déjà proche de collectors_core |
| time | generated_at / collected_at helpers | OUI | pur utilitaire |
| io | JSON / JSONL file helpers | OUI | déjà dans l'esprit collectors_core |
| http | retry/backoff wrapper commun | OUI SI duplication prouvée | éviter réécriture multiple |

## 2_NON EXTRACTIBLE

| Zone | Candidate | Pourquoi non |
|---|---|---|
| dérivés | funding / OI / liquidations semantics | métier spécifique |
| dérivés | adapters bitget/binance derivatives | provider-specific + métier |
| payload | normalized derivatives contracts | ne doit pas contaminer spot |
| exports | legacy JSON/CSV payload shapes | dépendances aval historiques |

## 3_EXTRACTION ORDER

```text
1. helpers lifecycle
2. helpers timestamps / file writing
3. helpers config non disruptifs
4. wrappers http seulement si duplication prouvée
```

## RISKS

- À qualifier.
