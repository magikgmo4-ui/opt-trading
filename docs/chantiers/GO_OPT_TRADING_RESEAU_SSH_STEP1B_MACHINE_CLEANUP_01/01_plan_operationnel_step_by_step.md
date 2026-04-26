---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01_PLAN
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - machine_cleanup
  - plan
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01/02_step_01_inventaire.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01/03_step_02_execution_cleanup.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01/90_closeout.md
---

# Plan operationnel step by step

## Step 01 - inventaire

- objectif : verifier la presence de `step1b` sur `db-layer`, `admin-trading`, `student`, `fantome`
- statut : complete

## Step 02 - cleanup borne

- objectif : deplacer les repertoires machine-side vers une archive locale datee
- statut : complete

## Step 03 - revalidation canonique

- objectif : verifier `baseline-*` et `sanity` apres cleanup
- statut : complete

## Step 04 - arbitrage environnement

- objectif : qualifier le gap `PyYAML` sur `fantome`
- statut : pending

## Target
1 module canonique par famille.
