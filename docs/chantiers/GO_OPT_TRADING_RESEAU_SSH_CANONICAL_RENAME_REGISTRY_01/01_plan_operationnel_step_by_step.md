---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - canonical
  - rename
  - registry
  - plan
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/02_step_01_move_execution.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/03_step_02_registry_alignment.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/04_step_03_active_docs_alignment.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/05_step_04_prepare_commits_pr.md
---

# Plan operationnel step-by-step

## Step 01 - move top-level
- statut : complete
- objectif : documenter la sortie du legacy step1 et la promotion repo-side du canonique

## Step 02 - alignement registre
- statut : complete
- objectif : porter `reseau_ssh` dans `modules_registry` et `wrappers_registry`

## Step 03 - alignement docs actives
- statut : complete
- objectif : realigner les surfaces actives sur `modules/reseau_ssh`

## Step 04 - preparation commits et PR
- statut : complete
- objectif : preparer un bundle Git propre sans execution

## Point de reprise
Le prochain lot utile n'est plus repo-side.

Le prochain lot utile est machine-side :
- repointage des alias courts
- rollback capture
- smoke tests par machine

## Target
1 module canonique par famille.
