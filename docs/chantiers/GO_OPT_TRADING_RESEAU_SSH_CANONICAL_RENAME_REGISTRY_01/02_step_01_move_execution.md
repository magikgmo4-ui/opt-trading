---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01_STEP_01_MOVE
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - canonical
  - move
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/README.md
  - _archive/legacy_modules/reseau_ssh_step1/README.md
---

# Step 01 - move execution

## Mouvement retenu
- ancien occupant top-level `modules/reseau_ssh` -> `_archive/legacy_modules/reseau_ssh_step1`
- ancienne base `modules/reseau_ssh_step2` -> `modules/reseau_ssh`

## Effet obtenu
- le nom canonique final `reseau_ssh` est libere puis recupere
- le legacy step1 sort de la surface active `modules/`
- la famille a maintenant un proprietaire top-level unique cote repo-side

## Point de vigilance
Le move top-level ne regle pas a lui seul :
- la publication machine-side des alias courts
- la baseline `step1b`

## Target
1 module canonique par famille.
