---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_STEP_04_EXIT_DECISION
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - compat
  - rollback
  - archive
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/01_inventaire_surfaces_compat.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/04_step_03_audit_wrappers_racine.md
---

# Step 04 - arbitrage de sortie

## Decision retenue

Etat de sortie intermediaire :
- `scripts/reseau_ssh` = `compat_active_backend`
- `scripts/reseau_ssh_cmd.sh` = `archive_backup`
- `scripts/reseau_ssh_menu.sh` = `archive_backup`

## Motif

Le dossier `scripts/reseau_ssh` conserve encore une valeur borne mais reelle :
- backend de compat encore appele par la facade canonique
- rollback
- lecture historique du backend legacy
- preuve de transition entre ancien runtime et canonique

En revanche, les wrappers racine historiques n'apportent plus de valeur operatoire prouvee.

## Ce qui est maintenant autorise

Cette decision a maintenant ete executee :
- `scripts/reseau_ssh_cmd.sh` archive
- `scripts/reseau_ssh_menu.sh` archive

## Ce qui reste interdit a ce stade

- archiver tout `scripts/reseau_ssh/` sans lot separe
- retirer la delegation compat de la facade sans lot borne
- retirer `modules/reseau_ssh_step1b`
- retirer les alias suffixes `*_reseau_ssh_step2`
- supprimer le rollback machine-side sans preuve complementaire

## Target
1 module canonique par famille.
