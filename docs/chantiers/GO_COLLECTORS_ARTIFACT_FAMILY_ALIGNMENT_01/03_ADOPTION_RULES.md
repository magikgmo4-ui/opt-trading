---
doc_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01_ADOPTION_RULES
doc_type: adoption_rules
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_adoption_rules
parent_go_id: GO_COLLECTORS_VOCABULARY_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - artifacts
  - adoption
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01/03_ADOPTION_RULES.md
point_de_reprise: "Définir les règles d’adoption additive de la famille d’artefacts."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01/02_DERIVATIVES_TO_FAMILY_MAP.md
---

# 03_ADOPTION_RULES

## 1_RULES

```text
R1. Introduire les artefacts famille sans casser les consumers aval.
R2. Garder les legacy outputs tant qu’un closeout n’a pas prouvé la bascule.
R3. Préférer l’addition d’enveloppes lifecycle à la refonte des payloads métier.
R4. Aligner la lecture docs/runbooks avant d’aligner les implémentations.
R5. Tout nouveau collector doit adopter la famille d’artefacts dès son ouverture.
```

## 2_NEXT STEP

```text
Après artifact family alignment :
- config boundary alignment
- operator surface alignment
- selective runtime extraction decision
```
