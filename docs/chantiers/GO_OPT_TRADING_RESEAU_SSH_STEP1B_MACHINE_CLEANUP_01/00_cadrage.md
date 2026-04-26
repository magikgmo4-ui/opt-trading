---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01
status: open
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - machine_cleanup
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01/03_step_02_execution_archive.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01 - Cadrage

## Objet

Sortir les repertoires `step1b` residuels des machines cibles sans toucher au canonique publie.

Le lot est machine-side uniquement.

## Etat de depart

- `step1b` est deja archive repo-side
- plus aucun alias `step1b` n'est publie sur les 4 hotes
- les repertoires `step1b` restent presents sur `db-layer`, `admin-trading`, `student`, `fantome`

## Cible

- move machine-side de `modules/reseau_ssh_step1b` vers une archive locale datee
- preservation d'un rollback explicite
- validation des commandes publiees `baseline-*` et `sanity`

## Target
1 module canonique par famille.
