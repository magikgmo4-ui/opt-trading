---
doc_id: GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01
parent_go_id: GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
status: open
lifecycle_stage: governance_alignment
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
topic_keys:
  - opt-trading
  - master_project_plan
  - go_structural_role
  - creation_rule
---

# GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01

## 1_MASTER_TARGET

Matrice étendue avec une règle de création qui impose le rôle structurel de chaque GO et le rattachement à la chaîne `PF_* -> 1_MASTER_TARGET -> 4_MASTER_PROJECT_PLAN -> parent -> child`.

## 3_INITIAL_NEED

Après la synchronisation des index globaux avec `MASTER_PROJECT_PLAN_INDEX`, il fallait fixer la méthode de création afin que les prochains GO soient typés dès l’ouverture.

## 4_MASTER_PROJECT_PLAN

- Ajouter la règle `GO_STRUCTURAL_ROLE`.
- Définir les rôles : `GO_CHILD`, `GO_CHILD_ATTACHED_TO_PARENT`, `GO_PARENT`, `GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN`, `GO_MASTER_PROJECT_PLAN`.
- Exclure `GO_ORPHAN` comme rôle canonique.
- Rendre obligatoire `NEXT_ATTACH_TARGET` pour les GO non encore rattachés.
- Définir l’index global comme `MASTER_PROJECT_PLAN_INDEX`.
- Rattacher support/tool/other à un parent de continuité puis à un `4_MASTER_PROJECT_PLAN`.

## 6_FINAL_TARGET

Publier l’extension canonique de matrice et le bundle associé, sans migration massive des anciens GO.

## 12_INVARIANTS

- Un child non rattaché est `GO_CHILD`, pas `GO_ORPHAN`.
- Un parent non rattaché est `GO_PARENT`, pas `GO_ORPHAN`.
- Un GO incomplet doit avoir `NEXT_ATTACH_TARGET`.
- Un parent ne ferme pas sans `PF_*`, `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN` et `CLOSE_GATE_MASTER_TARGET`.

## 17_RESUME_POINT

Prochain GO recommandé : appliquer cette règle aux prochaines ouvertures, puis corriger progressivement les anciens GO si nécessaire.
