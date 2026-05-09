---
doc_id: GO_COLLECTORS_VOCABULARY_ALIGNMENT_01_ADOPTION_RULES
doc_type: adoption_rules
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_VOCABULARY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_adoption_rules
parent_go_id: GO_COLLECTORS_BASELINE_INVENTORY_01
topic_keys:
  - opt-trading
  - collectors
  - adoption
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_VOCABULARY_ALIGNMENT_01/03_ADOPTION_RULES.md
point_de_reprise: "Definir comment adopter le vocabulaire sans casser les consumers existants."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_VOCABULARY_ALIGNMENT_01/02_CANONICAL_VOCABULARY_MAP.md
---

# 03_ADOPTION_RULES

## 1_REGLES

```text
R1. Aligner d'abord docs et runbooks.
R2. Introduire les noms canoniques en mode additif.
R3. Ne pas supprimer les legacy outputs pendant l'alignement vocabulaire.
R4. Ne pas forcer les modules derives a adopter collectors_core d'un coup.
R5. Toute evolution runtime future doit reutiliser ce vocabulaire.
```

## 2_NEXT_STEPS APRES VOCABULARY

```text
1. artifact family alignment
2. config boundary alignment
3. operator surface alignment
4. selective runtime extraction decision
```
