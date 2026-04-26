---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01_AUDIT
doc_type: chantier_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - audit
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/_reseau_ssh_common.sh
  - modules/reseau_ssh/scripts/capture_shortcuts_snapshot.sh
  - _archive/legacy_modules/reseau_ssh_step1b/README.md
---

# Audit de sortie step1b

## Constat

- aucun caller canonique ne depend plus de `modules/reseau_ssh_step1b`
- plus aucun alias `menu-reseau_ssh_step1b`, `cmd-reseau_ssh_step1b`, `sanity-reseau_ssh_step1b` n'est publie sur `db-layer`, `admin-trading`, `student`, `fantome`
- les references restantes sont historiques, documentaires, ou internes a l'archive

## Residus bornes

- des copies machine-side de `/opt/trading/modules/reseau_ssh_step1b` existent encore
- `capture_shortcuts_snapshot.sh` garde volontairement la sonde machine-side sur `/opt/trading/modules/reseau_ssh_step1b`
- le cleanup distant doit rester un lot separe

## Decision

- `step1b` peut sortir du flux actif du repo
- l'archive repo-side est autorisee
- le retrait machine-side est reporte a un runbook dedie

## Target
1 module canonique par famille.
