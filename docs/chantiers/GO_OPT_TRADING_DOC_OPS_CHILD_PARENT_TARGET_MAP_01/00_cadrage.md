---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01_CADRAGE
doc_type: chantier_child
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - doc_ops
  - parent_target_map
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
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01/02_execution_order.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01

## Classification

Doc-only / sous-go de cartographie cible / aucun runtime / aucune ouverture de parent.

## Parent actif

`GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`

## Etat reel apres merge PR #180

- `origin/sot/mainline` et `sot/mainline` sont alignes sur `6321e7f`.
- `6321e7f` est le merge de PR #180 depuis `go/GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01`.
- `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01` est maintenant merge et clos.
- `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`, `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`, `GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01` et `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01` ne doivent pas etre rouverts.

## Role du present GO

Produire la carte cible future des 5 parents project/machine a ouvrir plus tard, sans en ouvrir aucun dans ce lot, et sans lancer encore `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01`.

## Justification du passage a PARENT_TARGET_MAP

- `02_go_map.md` fixe `PARENT_TARGET_MAP` comme etape 4, apres `PRIMARY_RESTART` ;
- `90_closeout.md` et `02_execution_order.md` de `PRIMARY_RESTART` designent `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01` comme suite probable si PASS ;
- PR #180 a merge ce PASS sur `sot/mainline`, ce qui leve le dernier verrou de reprise avant la carte cible ;
- la cartographie des 5 parents doit preceder toute ouverture reelle pour eviter des parents decoratifs ou mal rattaches.

## Hypothese directrice repo-first

La carte cible la plus prouvable a ce stade est :

- 1 parent `PROJECT` oriente `localcms` ;
- 4 parents `MACHINE` ou `SUPPORT` orientes `admin-trading`, `db-layer`, `student`, `fantome`.

Cette hypothese doit etre justifiee et bornee dans `01_parent_target_map.md`.

## Anti-cibles

- aucun runtime ;
- aucune suppression de branche ;
- aucun merge secondaire ;
- aucune ouverture de parent ;
- aucun lancement de `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01`.

## Point de reprise

Lire `01_parent_target_map.md`, puis `02_validation_matrix.md`.

## RISKS

- À qualifier.
