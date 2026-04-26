---
doc_id: GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01_AUDIT
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01
status: complete
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - reseau_ssh
  - rollback
  - archive
  - audit
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/_reseau_ssh_common.sh
  - modules/reseau_ssh/scripts/cmd.sh
  - _archive/legacy_modules/reseau_ssh_runtime_rollback_only/README.md
---

# Audit repo-side

## Constat

Avant archivage :
- les seuls pointeurs code encore vivants vers `scripts/reseau_ssh` etaient dans `modules/reseau_ssh/scripts/_reseau_ssh_common.sh`
- et dans le message d'erreur de `modules/reseau_ssh/scripts/cmd.sh`

Ils ne correspondaient plus a une dependance runtime active.

## References restantes

Les references observees hors code actif sont :
- docs de chantier
- traces historiques
- notes de runtime anciennes

Conclusion :
- pas de caller repo-side actif critique a conserver
- archivage repo-side autorise

## Target
1 module canonique par famille.
