---
doc_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01
status: open
lifecycle_stage: cadrage_execution_future
topic_keys:
  - opt-trading
  - reseau_ssh
  - compat
  - backend
  - absorption
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/07_step_06_blocage_backend_compat.md
  - modules/reseau_ssh/scripts/cmd.sh
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
---

# GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01 - Cadrage

## Objet

Ouvrir le lot borne qui preparera la sortie de `scripts/reseau_ssh` du flux actif.

Ce lot ne vise pas l'archivage direct du backend compat.

Il vise d'abord :
- l'inventaire exact des commandes encore deleguees a `scripts/reseau_ssh`
- l'arbitrage `absorb`, `deprecate`, ou `keep-transition`
- la preparation des patches repo-side eventuels sur `modules/reseau_ssh/scripts/*`

## Etat de depart

Etat actuel retenu :
- `modules/reseau_ssh` = canonique
- aliases courts publies sur 4/4 hotes vers `modules/reseau_ssh/scripts/*`
- wrappers racine historiques archives
- `scripts/reseau_ssh` encore requis comme `compat_active_backend`

## Question centrale

Pour atteindre une famille vraiment canonique, il faut trancher commande par commande :
- que faut-il absorber dans `modules/reseau_ssh` ?
- que faut-il garder temporairement en compat ?
- que faut-il deprécier explicitement ?

## Point de reprise

La suite utile commence par une matrice de commandes :
- façade canonique
- implementation nested `step2`
- backend compat `scripts/reseau_ssh`
- transition `step1b`

## Target
1 module canonique par famille.
