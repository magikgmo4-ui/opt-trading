---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01_PLAN
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - plan
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01/01_audit_sortie.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01/03_step_02_execution_archive.md
---

# Plan operationnel step by step

## Step 01 - audit de sortie

- objectif : prouver l'absence de dependance canonique et d'alias publies
- statut : complete

## Step 02 - archive repo-side

- objectif : deplacer `modules/reseau_ssh_step1b` sous `_archive/legacy_modules/`
- statut : complete

## Step 03 - realignement des surfaces actives

- objectif : mettre a jour le canonique, le statut et les index de continuite
- statut : complete

## Step 04 - cleanup machine-side

- objectif : lot separe, non execute ici
- statut : pending

## Target
1 module canonique par famille.
