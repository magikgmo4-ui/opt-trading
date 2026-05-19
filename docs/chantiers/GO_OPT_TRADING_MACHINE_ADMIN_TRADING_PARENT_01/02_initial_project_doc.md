---
doc_id: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01_INITIAL_PROJECT_DOC
doc_type: projet_initial
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - machine
  - admin_trading
  - initial_project_doc
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md
point_de_reprise: "Section Axes initiaux"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md
---

# 02_initial_project_doc

## Perimetre retenu

Le parent `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` couvre la machine `admin-trading` comme surface machine autonome, sans prendre possession des chantiers transverses qui la traversent.

## Axes initiaux

1. qualifier les surfaces machine specifiques a `admin-trading` ;
2. distinguer ce qui releve du parent machine de ce qui reste dans `reseau_ssh`, `tmux-ide` ou d'autres chantiers transverses ;
3. preparer un futur enfant seulement si un besoin machine propre, stable et non decoratif est etabli.

## Non-scope immediat

- aucun changement runtime ;
- aucune migration SSH supplementaire ;
- aucune ouverture d'enfant dans ce lot ;
- aucune decision de branche dedicatee dans `BRANCH_STATE.md`.
