---
doc_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01_STEP_03_PATCH
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
  - patch
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/_reseau_ssh_transition.sh
  - modules/reseau_ssh/scripts/cmd.sh
---

# Step 03 - patch repo-side

## Patch applique

Le canonique `modules/reseau_ssh` porte maintenant directement :
- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`

Un helper shell canonique dedie a ete ajoute :
- `modules/reseau_ssh/scripts/_reseau_ssh_transition.sh`

La facade `cmd.sh` n'appelle plus le backend legacy pour ces trois commandes.

## Resultat

Le canonique `reseau_ssh` porte maintenant :
- la facade d'info et de lecture
- les commandes WireGuard et firewall `step2`
- les trois commandes de bootstrap / hardening SSH

`scripts/reseau_ssh` n'est plus necessaire pour la facade canonique.

## Target
1 module canonique par famille.
