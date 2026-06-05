---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01
status: complete
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - machine
  - runtime
  - plan
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/02_step_01_inventaire_et_rollback.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/03_step_02_runbook_db_layer.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/04_step_03_runbook_admin_trading.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/05_step_04_runbook_student.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/06_step_05_runbook_fantome.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/07_step_06_prepare_commits_pr.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/08_step_07_probe_connectivite.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/09_step_08_resultats_inventaire_reel.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md
---

# Plan operationnel step-by-step

## Step 01 - inventaire et rollback
- statut : complete
- objectif : fixer les commandes de snapshot avant toute action distante

## Step 02 - runbook `db-layer`
- statut : complete
- objectif : machine de preuve prioritaire, avec compat `step2` déjà plausible

## Step 03 - runbook `admin-trading`
- statut : complete
- objectif : cas central à fort impact opératoire

## Step 04 - runbook `student`
- statut : complete
- objectif : machine à risque plus élevé à cause de l’historique `step1b`

## Step 05 - runbook `fantome`
- statut : complete
- objectif : machine dev dédiée, à qualifier séparément sans la mélanger au cas `student`

## Step 06 - préparation commits et PR
- statut : complete
- objectif : préparer le bundle Git si un ajustement repo-side additionnel devient nécessaire après exécution machine

## Step 07 - probe de connectivité
- statut : complete
- objectif : prouver si la session courante peut atteindre les hôtes SSH avant toute exécution distante

## Step 08 - résultats d’inventaire réel
- statut : complete
- objectif : figer l’état observé machine par machine avant tout repointage

## Step 09 - résultats d’exécution
- statut : complete
- objectif : figer les machines effectivement migrées et les blocages restants

## Point de reprise
Le lot machine-side est execute sur :
- `db-layer`
- `admin-trading`
- `student`
- `fantome`

Point de reprise suivant :
- ouvrir le lot de reduction de compatibilite sur `scripts/reseau_ssh`
- qualifier ensuite le retrait progressif de `reseau_ssh_step1b`

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
