---
doc_id: GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01_PARENT
doc_type: chantier_parent
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - machine
  - db_layer
  - parent
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/00_cadrage.md
point_de_reprise: "Section TODO"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/00_cadrage.md
---

# GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01

## Classification

chantier parent machine + doc-only + cadrage operatoire

## Role recommande

parent canonique de la machine `db-layer` pour ses interfaces de consultation, d'export et d'ingestion

## Besoin initial

Ouvrir un parent machine compact pour `db-layer`, afin de disposer d'un point d'ancrage canonique sans melanger cette machine avec l'ensemble des familles data, reseau ou runtime.

## Cible finale

Disposer d'un parent machine qui :

- borne `db-layer` comme machine distincte ;
- rattache les futures decisions a une cible machine claire ;
- evite de transformer des preuves `reseau_ssh` en parent decoratif.

## Source canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`
- Support Git cible du parent : `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01`

## ETABLI

- `db-layer` est une machine prouvee et migree PASS dans les surfaces `reseau_ssh` ;
- la machine reste un pivot credible pour des flux export-consultation-ingestion ;
- ce parent est ouvert en doc-only via `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01`.

## Anti-cibles

Ne pas faire :

- requalifier toute la couche data du repo comme si elle appartenait a la machine `db-layer` ;
- deduire une modification machine ou runtime de cette ouverture documentaire ;
- ouvrir ici des enfants avant l'audit de conformite parent.

## GO suivants proposes

- inventaire machine et interfaces rattachees ;
- decisions de frontiere avec les chantiers transverses data / reseau / runtime ;
- eventuel enfant machine seulement si un axe autonome est prouve.

## TODO

- inventorier les surfaces machine reellement rattachees a `db-layer` ;
- documenter les interfaces de consultation, export et ingestion deja prouvees ;
- cadrer ce qui reste hors perimetre de ce parent.

## RISKS

- À qualifier.
