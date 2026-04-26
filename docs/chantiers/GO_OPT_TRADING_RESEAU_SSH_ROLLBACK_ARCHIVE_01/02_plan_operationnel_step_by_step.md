---
doc_id: GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - rollback
  - archive
  - plan
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01/01_audit_repo_side.md
---

# Plan operationnel step-by-step

## Step 01 - audit repo-side
- statut : complete
- objectif : verifier l'absence de caller actif critique

## Step 02 - move archive
- statut : complete
- objectif : deplacer `scripts/reseau_ssh` sous `_archive/legacy_modules/`

## Step 03 - realignement canonique
- statut : complete
- objectif : retirer les derniers pointeurs morts du canonique

## Step 04 - realignement docs actives
- statut : complete
- objectif : refléter l'archivage repo-side et la nouvelle reprise

## Point de reprise

Le prochain lot utile n'est plus `scripts/reseau_ssh`.

Le prochain lot utile est :
- qualification de `reseau_ssh_step1b`

## Target
1 module canonique par famille.
