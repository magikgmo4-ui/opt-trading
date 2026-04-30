---
doc_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02
status: draft
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - doc_ops
  - matrix_patch
  - parent_continuity
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02/01_PATCH_PROPOSAL.md
updated_at: 2026-04-30
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01.md
---

# GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02 — cadrage

## 1_MASTER_TARGET

Porter la règle de continuité locale des parents dans la couche gouvernance / matrice, sans transformer les index globaux en journal de micro-avancement.

## 3_INITIAL_NEED

Formaliser pour tous les prochains parents :

- continuité locale complète dans `docs/chantiers/<GO_PARENT>/` ;
- entrée atomique dans `docs/index/inbox/<GO_PARENT>.md` ;
- index globaux modifiés seulement par batch ou changement structurel.

## 7_CANONICAL_STATE

- Branche dédiée ouverte depuis `sot/mainline` courant.
- La matrice maître existe et reste la référence souveraine.
- Le connecteur GitHub ne permet pas ici une réécriture sûre partielle du gros fichier matrice sans remplacer tout le contenu.
- Ce lot crée donc un addendum gouvernance canonique candidat + une proposition de patch exact à intégrer dans la matrice.

## 17_RESUME_POINT

Lire `01_PATCH_PROPOSAL.md`, puis appliquer le bloc proposé dans `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` lors d'un passage local/rebase sûr.
