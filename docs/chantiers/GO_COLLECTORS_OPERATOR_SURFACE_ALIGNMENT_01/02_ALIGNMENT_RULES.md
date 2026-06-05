---
doc_id: GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01_ALIGNMENT_RULES
doc_type: alignment_rules
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_alignment_rules
parent_go_id: GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - operator-surface
  - alignment
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01/02_ALIGNMENT_RULES.md
point_de_reprise: "Fixer les regles d'alignement de la surface operateur collectors."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01/01_SURFACE_BASELINE.md
---

# 02_ALIGNMENT_RULES

## 1_RULES

```text
R1. Converger vers des attentes communes avant de changer les scripts.
R2. Accepter des noms provider-specific tant que le runbook est clair.
R3. Prioriser l'alignement documentation + menu + sanity avant toute refonte shell.
R4. collectors_core reste support package, pas point d'entree operateur principal.
R5. marketdata peut rester facade tant que la famille est lisible operatoirement.
```

## 2_FUTURE TARGET

```text
Une future phase d'implementation pourra introduire :
- conventions de nommage homogenes
- short aliases stables
- runbook templates communs
```

## RISKS

- À qualifier.
