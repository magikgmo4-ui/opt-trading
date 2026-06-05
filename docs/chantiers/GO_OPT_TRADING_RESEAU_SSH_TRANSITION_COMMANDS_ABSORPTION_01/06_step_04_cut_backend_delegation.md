---
doc_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01_STEP_04_CUT_BACKEND
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - transition
  - backend
  - menu
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/menu.sh
  - scripts/reseau_ssh/reseau_ssh_menu.sh
  - scripts/reseau_ssh/README_RUNTIME_STATUS.md
---

# Step 04 - cut backend delegation

## Execution

Le menu canonique `modules/reseau_ssh/scripts/menu.sh` n'ouvre plus le menu compat.

Le menu canonique expose maintenant directement :
- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`
- le menu WireGuard / firewall `step2`
- les commandes `step1b`

## Resultat

Il n'existe plus de delegation implicite depuis la surface canonique vers :
- `scripts/reseau_ssh/reseau_ssh_cmd.sh`
- `scripts/reseau_ssh/reseau_ssh_menu.sh`

Le dossier `scripts/reseau_ssh` change donc de statut :
- ancien : `keep-transition`
- nouveau : `rollback_only`

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
