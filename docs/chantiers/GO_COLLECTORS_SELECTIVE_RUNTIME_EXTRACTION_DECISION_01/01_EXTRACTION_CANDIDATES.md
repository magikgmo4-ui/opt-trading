---
doc_id: GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01_EXTRACTION_CANDIDATES
doc_type: extraction_candidates
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01
status: draft_for_review
lifecycle_stage: child_candidates
parent_go_id: GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - extraction
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/01_EXTRACTION_CANDIDATES.md
point_de_reprise: "Lister ce qui pourrait etre extrait selectivement, et ce qui doit rester separe."
updated_at: 2026-05-07
links:
  - docs/COLLECTORS_FAMILY_DOCTRINE_01.md
---

# 01_EXTRACTION_CANDIDATES

## 1_POTENTIELLEMENT EXTRACTIBLE

```text
- helpers lifecycle compatibles famille
- wrappers d'ecriture manifest/status/latest/events/errors
- conventions de timestamps et run identity
- couches config si elles sont generiques
- wrappers HTTP/retry si une duplication reelle est prouvee
```

## 2_DOIT RESTER SEPARE

```text
- semantics derives
- adapters provider-specific derives
- payloads metier derives
- normalized contracts derives
- downstream expectations derives
```

## RISKS

- À qualifier.
