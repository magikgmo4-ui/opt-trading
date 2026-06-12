---
doc_id: GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01_INITIAL_PROJECT_DOC
doc_type: projet_initial
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - machine
  - db_layer
  - initial_project_doc
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md
point_de_reprise: "Section Axes initiaux"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md
---

# 02_initial_project_doc

## Perimetre retenu

Le parent `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` couvre la machine `db-layer` comme machine autonome, sans prendre a sa charge l'ensemble des familles data ou runtime du repo.

## Axes initiaux

1. qualifier les interfaces machine specifiques a `db-layer` ;
2. distinguer ce qui releve de la machine de ce qui reste transverse ;
3. preparer un futur enfant seulement si un besoin machine stable et non decoratif se confirme.

## Non-scope immediat

- aucun patch runtime ;
- aucune bascule de pipeline ;
- aucune ouverture d'enfant dans ce lot ;
- aucune mise a jour de `BRANCH_STATE.md`.

## RISKS

- À qualifier.
