---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01_CADRAGE
doc_type: chantier_child
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - doc_ops
  - primary_restart
  - project_machine_split
  - continuity
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Point de reprise"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01/02_next_flow_arbitration.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01

## Classification

Doc-only / sous-go de reprise operatoire unique / aucun runtime / aucune suppression de branche.

## Parent actif

`GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`

## Etat reel apres merge PR #179

- `origin/sot/mainline` et `sot/mainline` sont alignes sur `fe42d78`.
- `fe42d78` est le merge de PR #179 depuis `go/GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01`.
- `GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01` est maintenant merge et clos.
- `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` ne doit pas etre rouvert.
- `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` ne doit pas etre rouvert.
- `GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01` ne doit pas etre rouvert.

## Role du present GO

Formaliser pourquoi `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01` devient maintenant le prochain flux operatoire unique du parent, malgre la presence d'autres P0 actifs dans le repo.

## P0 en concurrence lus dans le repo

- `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`
- `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01`
- `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`
- `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`

## Flux unique retenu maintenant

`GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01`

## Pourquoi maintenant

- le parent `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` porte une sequence canonique explicite dans `02_go_map.md` ;
- cette sequence a deja consomme `BRANCH_CLEANUP`, `OPEN_WORK_CONTROL` puis `CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL` ;
- le closeout du GO precedent et son arbitrage repo-first designent `PRIMARY_RESTART` comme suite naturelle ;
- `PRIMARY_RESTART` doit etre formalise avant tout `PARENT_TARGET_MAP` et avant toute ouverture des 5 parents project/machine ;
- les autres P0 restent ouverts, mais ils n'annulent pas la chaine de reprise explicite de ce parent.

## Explicitement reporte

- `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01`
- `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01`
- l'ouverture des 5 parents project/machine

## Anti-cibles

- aucun runtime ;
- aucune suppression de branche ;
- aucun merge de branche secondaire ;
- aucun push ;
- aucune ouverture de `PARENT_TARGET_MAP` ;
- aucune ouverture des 5 parents project/machine.

## Point de reprise

Lire `01_restart_arbitration.md`, puis `02_execution_order.md`.
