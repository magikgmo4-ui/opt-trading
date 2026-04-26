---
doc_id: GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01_EXECUTION
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - rollback
  - archive
  - execution
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - _archive/legacy_modules/reseau_ssh_runtime_rollback_only/README.md
  - modules/reseau_ssh/scripts/_reseau_ssh_common.sh
  - modules/reseau_ssh/scripts/cmd.sh
---

# Step 02 - execution archive

## Execution

Le dossier repo-side :
- `scripts/reseau_ssh/`

a ete deplace vers :
- `_archive/legacy_modules/reseau_ssh_runtime_rollback_only/`

Le canonique `modules/reseau_ssh` ne pointe plus vers cette surface archivee.

## Resultat

- le repo ne porte plus de surface active `scripts/reseau_ssh`
- l'archive repo-side reste disponible pour lecture ou restauration explicite
- la reprise de famille se concentre maintenant sur `modules/reseau_ssh` et `reseau_ssh_step1b`

## Target
1 module canonique par famille.
