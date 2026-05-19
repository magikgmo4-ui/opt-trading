---
doc_id: GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01_ADOPTION_RULES
doc_type: adoption_rules
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_adoption_rules
parent_go_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - config
  - adoption
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01/02_ADOPTION_RULES.md
point_de_reprise: "Definir l'adoption progressive de la boundary config collectors."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01/01_BOUNDARY_MAP.md
---

# 02_ADOPTION_RULES

## 1_RULES

```text
R1. Tout nouveau collector adopte la target boundary des son ouverture.
R2. derivatives_collector peut rester temporairement sur une couche de compatibilite documentee.
R3. Les secrets restent hors repo, quel que soit le collector.
R4. Les overrides machine-local doivent rester explicitement separes des defaults versionnes.
R5. Les env overrides servent a surcharger, pas a remplacer la doctrine.
```

## 2_EXPECTED RESULT

```text
La famille collectors dispose d'une doctrine config explicite et partagee,
sans refonte disruptive du runtime existant.
```
