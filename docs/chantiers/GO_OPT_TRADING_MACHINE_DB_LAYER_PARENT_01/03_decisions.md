---
doc_id: GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01_DECISIONS
doc_type: decision_log
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - machine
  - db_layer
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/02_initial_project_doc.md
point_de_reprise: "Section Suite"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/02_initial_project_doc.md
---

# 03_decisions

## Etabli

- le parent est ouvert doc-only ;
- `db-layer` est une machine suffisamment prouvee pour un parent autonome ;
- l'ouverture n'autorise aucun changement runtime ni reseau.

## Hypothese

- un futur GO enfant machine-first deviendra utile si un axe `db-layer` stable apparait hors des chantiers transverses deja ouverts.

## Interdit

- lire `db-layer` comme parent de toute la couche data du repo ;
- deduire une execution machine de cette seule ouverture documentaire.

## Suite

- attendre la validation du lot d'ouverture parent ;
- passer ensuite par le futur audit de conformite parent avant toute ouverture d'enfant.

## RISKS

- À qualifier.
