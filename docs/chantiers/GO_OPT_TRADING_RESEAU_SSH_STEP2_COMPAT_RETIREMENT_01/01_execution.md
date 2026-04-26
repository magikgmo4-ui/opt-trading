---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP2_COMPAT_RETIREMENT_01_EXECUTION
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP2_COMPAT_RETIREMENT_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step2
  - compat
  - retirement
  - execution
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - registry/wrappers_registry.yaml
  - modules/reseau_ssh/scripts/install_shortcuts.sh
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/install_shortcuts_linux.sh
---

# Execution

## Repo-side

- suppression des wrappers suffixes `cmd/menu/sanity-reseau_ssh_step2` dans `registry/wrappers_registry.yaml`
- `modules/reseau_ssh/scripts/install_shortcuts.sh` ne republie plus `step2` et delegue maintenant vers l'installateur canonique
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/install_shortcuts_linux.sh` est requalifie en redirecteur vers l'installateur canonique
- `capture_shortcuts_snapshot.sh` ne traite plus les alias suffixes comme surface active

## Machine-side

Suppression des alias suffixes sur :
- `db-layer`
- `admin-trading`
- `student`
- `fantome`

Archivage machine-side des anciens dossiers :
- `/opt/trading/_archive/legacy_modules/reseau_ssh_step2_machine_2026-04-25_final`
- `/home/fantome/opt-trading/_archive/legacy_modules/reseau_ssh_step2_machine_2026-04-25_final`

## Validation

Les 4 hotes ne publient plus que :
- `menu-reseau_ssh`
- `cmd-reseau_ssh`
- `sanity-reseau_ssh`

Les 4 hotes valident `sanity-reseau_ssh`.

## Target
1 module canonique par famille.
