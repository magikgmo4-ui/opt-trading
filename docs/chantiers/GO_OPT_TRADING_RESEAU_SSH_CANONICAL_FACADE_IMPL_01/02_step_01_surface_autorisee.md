---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01_STEP_01_SCOPE
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - facade
  - scope
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/menu.sh
  - modules/reseau_ssh/scripts/sanity_check.sh
  - modules/reseau_ssh/scripts/install_shortcuts.sh
  - modules/reseau_ssh/README.md
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/README.md
---

# Step 01 - surface autorisee

## Fichiers code autorises
- `modules/reseau_ssh/scripts/_reseau_ssh_common.sh`
- `modules/reseau_ssh/scripts/cmd.sh`
- `modules/reseau_ssh/scripts/menu.sh`
- `modules/reseau_ssh/scripts/sanity_check.sh`

## Fichiers doc autorises
- `modules/reseau_ssh/README.md`
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/README.md`
- dossier chantier courant

## Fichiers explicitement geles
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/*`
- `modules/reseau_ssh_step1b/**`
- `scripts/reseau_ssh/**`
- `registry/*.yaml`

## Regle
Le lot rend la facade top-level publiable cote repo sans modifier encore :
- le repointage machine-side
- la baseline `step1b`
- le backend compat

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
