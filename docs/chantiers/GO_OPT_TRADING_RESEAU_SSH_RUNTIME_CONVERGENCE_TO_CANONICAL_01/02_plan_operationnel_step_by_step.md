---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - runtime
  - convergence
  - plan
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/01_matrice_capacites.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/03_step_02_matrice_alias_wrappers.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/04_step_03_strategie_absorption.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/05_step_04_plan_bascule_alias_courts.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md
---

# Plan operationnel step-by-step

## Step 01 - matrice de capacites
- statut : complete
- objectif : comparer facade canonique, implementation interne, baseline compat et runtime historique

## Step 02 - matrice alias et wrappers
- statut : complete
- objectif : lister les publicateurs reels des alias courts et suffixes

## Step 03 - strategie d'absorption
- statut : complete
- objectif : fixer la facade canonique finale et la place des compatibilites

## Step 04 - plan de bascule
- statut : complete
- objectif : separer clairement repo-side, registre et machine-side

## Point de reprise
Le travail repo-side est maintenant segmente en deux lots :
- `GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01`
- `GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01`

Le lot restant apres eux est machine-side :
- repointer `menu/cmd/sanity-reseau_ssh`
- capturer rollback et smoke tests par machine

## Target
1 module canonique par famille.
