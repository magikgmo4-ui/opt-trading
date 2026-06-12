---
doc_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01_STEP_02_TARGET
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
  - target
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01/01_matrice_transition.md
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/menu.sh
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
---

# Step 02 - arbitrage de cible

## Decision

Les trois commandes restantes restent dans la famille `reseau_ssh` et doivent etre absorbees dans `modules/reseau_ssh`.

Commandes concernees :
- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`

## Motif

- elles sont deja publiees via `cmd-reseau_ssh`
- elles sont prouvees utiles sur les machines cibles
- leur code est borne, shell-only, et depend d'helpers simples
- les sortir vers une autre famille casserait la coherence de l'operateur `reseau_ssh` a ce stade

## Frontiere

L'absorption vise :
- la facade canonique `modules/reseau_ssh/scripts/cmd.sh`
- eventuellement un helper shell canonique dedie
- le menu canonique `modules/reseau_ssh/scripts/menu.sh`

Elle ne vise pas :
- la republication des anciennes commandes WireGuard retirees
- la suppression immediate de `scripts/reseau_ssh`
- la suppression immediate de `reseau_ssh_step1b`

## Point de reprise

Le prochain step utile est repo-side :
- absorber les helpers shell necessaires
- implementer les trois commandes dans le canonique
- retirer ensuite la delegation residuelle vers le backend compat

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
