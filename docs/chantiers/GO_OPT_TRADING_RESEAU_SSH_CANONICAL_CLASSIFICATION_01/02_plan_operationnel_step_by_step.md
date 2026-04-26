---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - modules
  - canonical
  - plan
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01/01_inventaire_et_classement_initial.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01/04_step_02_audit_blocage_runtime.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01/05_step_03_decision_convergence.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/02_plan_operationnel_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md
---

# Plan operationnel step-by-step

## Step 01 - classement modules
- statut : complete
- objectif : fixer le classement canonique / compat / archive de la famille

## Step 02 - audit du blocage runtime
- statut : complete
- objectif : documenter la dissociation entre canonique repo-side et publication machine-side

## Step 03 - decision de convergence
- statut : complete
- objectif : fixer `reseau_ssh` comme nom canonique final et borner les couches internes / compat

## Step 04 - preparation archive
- statut : in_progress
- objectif : garder `step1b` et `scripts/reseau_ssh` en compat seulement tant que les references actives ne sont pas coupees

Etat atteint :
- `reseau_ssh_step1` est deja archive
- `reseau_ssh` est deja le canonique top-level
- reste a traiter la publication machine-side et la dette de compat

## Point de reprise
Sous-lots actifs derives :
- `GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01`
- `GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01`

Suite logique :
- finaliser l'alignement repo-side et registre
- puis ouvrir le lot machine-side de repointage des alias courts

## Target
1 module canonique par famille.
