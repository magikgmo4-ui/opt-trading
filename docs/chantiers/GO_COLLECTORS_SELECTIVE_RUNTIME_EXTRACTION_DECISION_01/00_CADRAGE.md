---
doc_id: GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - selective-extraction
  - decision
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/00_CADRAGE.md
point_de_reprise: "Statuer s'il faut extraire selectivement une partie du runtime derivatives vers collectors_core."
updated_at: 2026-05-07
links:
  - docs/COLLECTORS_MIGRATION_MAP_01.md
  - docs/chantiers/GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01

## 1_MASTER_TARGET

Décider si une extraction runtime sélective depuis `derivatives_collector` vers `collectors_core` est utile, proportionnée, et sûre.

## 2_RULE

```text
Ce GO est un gate de decision, pas une migration automatique.
```

## 3_SCOPE

```text
INCLUS : coût/bénéfice, zones extractibles, zones interdites, décision explicite.
EXCLUS : refactor runtime, migration code, schema unification.
```

## RISKS

- À qualifier.
