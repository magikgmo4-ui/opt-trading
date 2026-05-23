# TARGETS — GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01

## 1_MASTER_TARGET

Matrice enrichie avec une règle de création qui force le typage structurel des GO et leur rattachement à la continuité `PF_* -> 1_MASTER_TARGET -> 4_MASTER_PROJECT_PLAN -> parent -> child`.

## 4_MASTER_PROJECT_PLAN

- Définir les rôles structurels autorisés.
- Exclure `GO_ORPHAN` comme rôle canonique.
- Imposer `NEXT_ATTACH_TARGET` aux GO non encore rattachés.
- Définir les champs minimaux à déclarer à la création.
- Confirmer `index global = MASTER_PROJECT_PLAN_INDEX`.
- Préparer une application progressive sans migration massive immédiate.

## 6_FINAL_TARGET

Publier l’extension canonique de matrice et les artefacts de bundle associés.

## BUNDLE_TARGET

Patch doc-only contenant :

- extension de matrice `MATRICE_DOC_OPS_MASTER_MATRIX_01_MASTER_PROJECT_PLAN_CREATION_RULE_01.md` ;
- dossier chantier ;
- entrée inbox ;
- bundle + target_card ;
- patch canonique archivé.

## Non-objectifs

- Ne migre pas tous les anciens GO.
- Ne ferme aucun parent.
- Ne modifie aucun runtime.
- Ne change pas les index globaux déjà synchronisés par #734.
