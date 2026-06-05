---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01_EXTRACTION_RULES
doc_type: extraction_rules
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
status: draft_for_review
lifecycle_stage: child_extraction_rules
parent_go_id: GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01
topic_keys:
  - opt-trading
  - collectors
  - extraction-rules
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01/02_EXTRACTION_RULES.md
point_de_reprise: "Règles pour un futur lot d'extraction helpers."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01/01_CANDIDATES_MATRIX.md
---

# 02_EXTRACTION_RULES

## 1_RULES

```text
R1. Toute extraction doit être bornée à un helper générique isolé.
R2. Toute extraction doit être additive avant d'être substitutive.
R3. Aucun consumer aval historique ne doit perdre ses outputs.
R4. Aucune sémantique dérivés ne doit être déplacée vers collectors_core.
R5. Chaque extraction future doit avoir son propre closeout.
```

## 2_NEXT STEP

```text
GO_COLLECTORS_HELPER_EXTRACTION_IMPL_01
```

Condition :

```text
choisir un helper concret et isolé (manifest/status/latest writers en premier).
```

## RISKS

- À qualifier.
