---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01_EXECUTION_ORDER
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - primary_restart
  - execution_order
  - project_machine_split
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01/01_restart_arbitration.md
point_de_reprise: "Ordre retenu"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01/90_closeout.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# 02_execution_order

## Ordre retenu dans la chaine parent

1. `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` : clos, non rouvert.
2. `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` : clos, non rouvert.
3. `GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01` : merge par PR #179, clos.
4. `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01` : present GO, flux unique retenu maintenant.
5. `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01` : explicitement reporte jusqu'au PASS du present GO.
6. `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01` : explicitement reporte.
7. ouverture des 5 parents project/machine : explicitement reportee.

## Effet attendu du present GO

- figer un seul point de depart operatoire pour la suite du parent ;
- rappeler pourquoi les autres P0 ne sont pas le flux unique de cette chaine ;
- documenter les conditions minimales avant tout passage a `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01`.

## Conditions de passage au GO suivant

Le GO suivant ne peut devenir ouvrable que si :

- le present GO est documente et verifie en doc-only ;
- `NEXT_GO_CANDIDATES.md`, `ACTIVE_STREAMS.md`, `REPRISE.md` et `GO_INDEX.md` refletent `PRIMARY_RESTART` comme flux courant ;
- `BRANCH_STATE.md` reste inchange comme surface branches seulement ;
- aucun runtime n'est touche ;
- aucune branche n'est supprimee ;
- aucune demande d'ouverture des 5 parents project/machine n'est introduite dans ce lot.

## GO suivant probable si PASS

`GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01`

## Interdits jusqu'au GO suivant

- ouvrir `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01` dans ce lot ;
- ouvrir `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01` dans ce lot ;
- ouvrir les 5 parents project/machine ;
- requalifier `BRANCH_STATE.md` comme surface de continuite produit.
