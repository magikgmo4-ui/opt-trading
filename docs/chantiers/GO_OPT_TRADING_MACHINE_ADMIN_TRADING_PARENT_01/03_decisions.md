---
doc_id: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01_DECISIONS
doc_type: decision_log
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - machine
  - admin_trading
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/02_initial_project_doc.md
point_de_reprise: "Section Suite"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/02_initial_project_doc.md
---

# 03_decisions

## Etabli

- le parent est ouvert doc-only ;
- `admin-trading` est une machine suffisamment prouvee pour un parent autonome ;
- l'ouverture ne cree aucun droit a modifier le runtime ni `BRANCH_STATE.md`.

## Hypothese

- un futur GO enfant machine-first deviendra utile si une surface `admin-trading` propre et durable apparait hors des chantiers transverses deja ouverts.

## Interdit

- absorber les preuves transverses comme si elles appartenaient entierement au parent ;
- deduire une execution machine de cette seule ouverture documentaire.

## Suite

- attendre la validation du lot d'ouverture parent ;
- passer ensuite par le futur audit de conformite parent avant toute ouverture d'enfant.
