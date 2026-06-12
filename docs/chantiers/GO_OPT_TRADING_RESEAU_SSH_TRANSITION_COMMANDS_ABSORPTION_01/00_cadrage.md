---
doc_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01
status: open
lifecycle_stage: cadrage_execution_future
topic_keys:
  - opt-trading
  - reseau_ssh
  - transition
  - bootstrap
  - hardening
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01/06_step_04_cut_deprecated_delegations.md
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/menu.sh
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
---

# GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01 - Cadrage

## Objet

Traiter les trois commandes encore publiees via le backend de transition :
- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`

Le but n'est pas de les laisser indefiniment dans `scripts/reseau_ssh`.

Le but est de decider puis executer une seule trajectoire canonique :
- absorption directe dans `modules/reseau_ssh`
- ou sortie explicite de la famille `reseau_ssh`

## Etat de depart

Etat actuel retenu :
- `modules/reseau_ssh` = module canonique publie sur les 4 hotes cibles
- `scripts/reseau_ssh` = backend `keep-transition`
- `wg-server-init`, `wg-client-init`, `wg-add-peer` = coupes de la facade canonique
- reste a traiter seulement `bootstrap`, `ssh-hardening-safe`, `ssh-lockdown`

## Question centrale

Ces trois commandes sont prouvees utiles, mais elles ne doivent plus vivre en delegation implicite permanente.

Il faut donc trancher :
- absorption dans la facade canonique
- reclassification hors famille `reseau_ssh`
- ou retrait pur si elles ne sont plus necessaires

## Point de reprise

Le lot commence par une matrice de role et d'ownership :
- code reel
- dependances shell
- impact machine-side
- cible canonique finale

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
