---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01
topic_keys:
  - opt-trading
  - collectors
  - helper-extraction
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01/00_CADRAGE.md
point_de_reprise: "Identifier les helpers extractibles sans toucher aux semantics derives."
updated_at: 2026-05-07
links:
  - docs/COLLECTORS_MIGRATION_MAP_01.md
---

# 00_CADRAGE — GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01

## 1_MASTER_TARGET

Identifier précisément quels helpers génériques pourraient être extraits vers `collectors_core`, sans toucher aux sémantiques métier dérivés.

## 2_RULE

```text
Helpers only.
Pas d'extraction de logique métier.
Pas de migration runtime.
Pas de broad refactor.
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 code move
- 0 schema change
```

## RISKS

- À qualifier.
