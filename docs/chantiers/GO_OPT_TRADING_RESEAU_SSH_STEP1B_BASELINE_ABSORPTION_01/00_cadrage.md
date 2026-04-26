---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_BASELINE_ABSORPTION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_BASELINE_ABSORPTION_01
status: open
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - baseline
  - absorption
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/reseau_ssh_cmd.sh
---

# GO_OPT_TRADING_RESEAU_SSH_STEP1B_BASELINE_ABSORPTION_01 - Cadrage

## Objet

Absorber dans `modules/reseau_ssh` les commandes `baseline-*` encore publiées via `reseau_ssh_step1b`.

Le but n'est pas encore d'archiver tout `step1b`.

Le but est de retirer sa dernière dépendance implicite depuis le canonique.

## Etat de depart

- `baseline-dry-run`
- `baseline-apply`
- `baseline-hostname`
- `baseline-sanity`
- `baseline-show-hosts`
- `baseline-show-ssh`

sont encore déléguées vers `modules/reseau_ssh_step1b`.

## Cible

- absorption dans `modules/reseau_ssh`
- plus aucun appel canonique vers `step1b`
- `step1b` requalifié en `archive_candidate`

## Target
1 module canonique par famille.
