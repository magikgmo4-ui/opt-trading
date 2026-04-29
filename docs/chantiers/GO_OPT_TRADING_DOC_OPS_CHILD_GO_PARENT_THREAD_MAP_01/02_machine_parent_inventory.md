---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01_MACHINE_PARENT_INVENTORY
doc_type: inventaire
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - machine
  - parent
  - admin_trading
  - db_layer
  - student
  - fantome
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Tableau parents machine"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/90_closeout.md
---

# 02_machine_parent_inventory — Inventaire des parents machine

## Regle

Les parents machine sont traites separes des parents gouvernance/projet. Ils representent une machine physique ou logique distincte dans l'infrastructure opt-trading.

## Tableau parents machine

| parent_id | machine | statut | dossier_present | ouvert_via | conformite_audit | fil_de_continuite |
| --- | --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | admin-trading | OPEN | oui | CHILD_PARENT_OPENING_BATCH_01 | PASS (CHILD_PARENT_CONFORMITY_AUDIT_01) | parent -> inventaire machine -> interfaces operateur -> futur enfant |
| GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | db-layer | OPEN | oui | CHILD_PARENT_OPENING_BATCH_01 | PASS (CHILD_PARENT_CONFORMITY_AUDIT_01) | parent -> inventaire machine -> interfaces consultation/export/ingestion -> futur enfant |
| GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01 | student | DEFERRED | non | — | — | differe ; pas de dossier ; pas ouvrir |
| GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01 | fantome | DEFERRED | non | — | — | differe ; pas de dossier ; pas ouvrir |

## Observations

### admin-trading
- machine prouvee dans les surfaces reseau_ssh
- alias courts migres PASS
- reaparait comme cible tmux-ide
- parent ouvert en doc-only
- pas d'enfant ouvert dans ce lot
- interfaces : operateur, desk, SSH, tmux

### db-layer
- machine prouvee et migree PASS dans reseau_ssh
- pivot export-consultation-ingestion
- parent ouvert en doc-only
- pas d'enfant ouvert dans ce lot
- interfaces : consultation, export, ingestion, SSH

### student
- differe explicitement dans GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01
- confirmee differee dans CHILD_PARENT_CONFORMITY_AUDIT_01
- pas de dossier parent present
- ne pas ouvrir dans ce lot

### fantome
- differe explicitement dans GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01
- confirmee differee dans CHILD_PARENT_CONFORMITY_AUDIT_01
- pas de dossier parent present
- ne pas ouvrir dans ce lot

## Contraintes

- un parent machine ne doit pas absorber les GO projet ou gouvernance
- un GO machine ne doit pas etre deplace vers un parent machine sans preuve
- les parents machine restent doc-only sauf instruction runtime explicite
