---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_04_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_04
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - helper-extraction
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_04/00_CADRAGE.md
point_de_reprise: "Extraire les builders manifest/latest generiques partages par les collecteurs spot."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_03/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_HELPER_EXTRACTION_IMPL_04

## 1_MASTER_TARGET

Extraire dans `collectors_core.lifecycle` les builders génériques `manifest` et `latest` communs aux collecteurs spot.

## 12_INVARIANTS

```text
- pas de logique métier déplacée
- builders génériques seulement
- pas de changement de payload métier
```

## RISKS

- À qualifier.
