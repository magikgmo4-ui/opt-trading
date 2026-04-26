---
doc_id: GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01
status: open
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - rollback
  - archive
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/_reseau_ssh_common.sh
  - _archive/legacy_modules/reseau_ssh_runtime_rollback_only/README.md
---

# GO_OPT_TRADING_RESEAU_SSH_ROLLBACK_ARCHIVE_01 - Cadrage

## Objet

Sortir `scripts/reseau_ssh` du flux actif du repo et le basculer en archive repo-side.

Le runtime legacy peut rester present sur machine pour rollback local, mais il ne doit plus exister comme surface active dans le repo.

## Etat de depart

- la facade canonique `modules/reseau_ssh` ne depend plus de `scripts/reseau_ssh`
- les aliases courts publies sur les 4 hotes cibles pointent deja vers `modules/reseau_ssh/scripts/*`
- `scripts/reseau_ssh` n'est plus qu'une surface `rollback_only`

## Cible

- move repo-side vers `_archive/legacy_modules/reseau_ssh_runtime_rollback_only/`
- suppression des pointeurs morts dans la facade canonique
- realignement des docs actives

## Target
1 module canonique par famille.
