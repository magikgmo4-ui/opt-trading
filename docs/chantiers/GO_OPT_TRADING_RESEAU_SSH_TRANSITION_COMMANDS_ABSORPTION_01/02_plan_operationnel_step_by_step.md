---
doc_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - transition
  - plan
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01/01_matrice_transition.md
---

# Plan operationnel step-by-step

## Step 01 - audit de role
- statut : complete
- objectif : confirmer code, dependances et utilite reelle des trois commandes restantes

## Step 02 - arbitrage de cible
- statut : complete
- objectif : trancher pour chaque commande entre :
  - `absorb_dans_canonique`
  - `extraire_hors_famille`
  - `retirer`

## Step 03 - patch repo-side
- statut : complete
- objectif : implementer la cible retenue dans `modules/reseau_ssh`

## Step 04 - reduction backend compat
- statut : complete
- objectif : retirer la delegation residuelle depuis `modules/reseau_ssh/scripts/cmd.sh` et `menu.sh`

## Step 05 - preparation Git
- statut : complete
- objectif : preparer commits et PR sans execution

## Point de reprise

Le point de reprise est maintenant post-absorption :
- `scripts/reseau_ssh` est `rollback_only`
- le prochain lot utile est la qualification finale `rollback_only` -> `archive_backup`
- ou l'arbitrage de `reseau_ssh_step1b`

## Target
1 module canonique par famille.
