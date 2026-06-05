---
doc_id: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01_PARENT
doc_type: chantier_parent
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - machine
  - admin_trading
  - parent
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/00_cadrage.md
point_de_reprise: "Section TODO"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md
---

# GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01

## Classification

chantier parent machine + doc-only + cadrage operatoire

## Role recommande

parent canonique de la machine `admin-trading` pour ses interfaces, son role operateur et ses futurs lots documentaires dedies

## Besoin initial

Isoler la lecture canonique de `admin-trading` dans un parent machine explicite, sans la dissoudre dans `reseau_ssh`, `tmux-ide` ou un chantier runtime transverse.

## Cible finale

Disposer d'un parent machine autonome qui :

- borne le perimetre de `admin-trading` ;
- relie proprement ses preuves machine, ses interfaces et ses futurs GO enfants ;
- evite de melanger SSH, UI, tmux et runtime dans un meme flux non qualifie.

## Source canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`
- Support Git cible du parent : `go/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01`

## ETABLI

- `admin-trading` est une machine prouvee dans les surfaces `reseau_ssh` ;
- les alias courts `reseau_ssh` y sont migres avec PASS ;
- la machine reapparait comme cible de travail credite dans les surfaces `tmux-ide` ;
- ce parent est ouvert en doc-only depuis `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01`.

## Anti-cibles

Ne pas faire :

- absorber tout `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` ;
- deduire une modification runtime de la seule ouverture de ce parent ;
- melanger le role machine `admin-trading` avec le parent `localcms` ou avec `db-layer`.

## GO suivants proposes

- inventaire machine et interfaces actives ;
- cadrage des surfaces operateur propres a `admin-trading` ;
- decisions de frontiere avec les chantiers transverses deja ouverts.

## TODO

- inventorier les surfaces machine reellement rattachees a `admin-trading` ;
- expliciter les interfaces operateur a garder sous ce parent ;
- borner les recouvrements avec `reseau_ssh` et `tmux-ide`.

## RISKS

- À qualifier.
