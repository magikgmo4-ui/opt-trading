---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP2_COMPAT_RETIREMENT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP2_COMPAT_RETIREMENT_01
status: open
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step2
  - compat
  - retirement
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/install_shortcuts.sh
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/install_shortcuts_linux.sh
  - registry/wrappers_registry.yaml
---

# GO_OPT_TRADING_RESEAU_SSH_STEP2_COMPAT_RETIREMENT_01 - Cadrage

## Objet

Retirer la compatibilite suffixee `*_reseau_ssh_step2` pour aboutir a une seule surface publiee `reseau_ssh`.

## Etat de depart

- le repo ne portait deja plus qu'un module top-level actif : `modules/reseau_ssh`
- le registre publiait encore `cmd/menu/sanity-reseau_ssh_step2`
- `db-layer` et `student` exposaient encore les alias suffixes
- les 4 hotes gardaient encore un ancien dossier machine-side `modules/reseau_ssh_step2`

## Cible

- retirer `*_reseau_ssh_step2` du registre et des installeurs
- supprimer les alias suffixes des 4 hotes
- archiver les anciens dossiers machine-side `reseau_ssh_step2`
- ne garder qu'un seul module physique actif et un seul jeu de menus publies

## Target
1 module canonique par famille.
