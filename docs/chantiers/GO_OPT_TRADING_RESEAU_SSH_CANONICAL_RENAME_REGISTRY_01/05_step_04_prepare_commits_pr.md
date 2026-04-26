---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01_STEP_04_PREPARE_GIT
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
  - commits
  - pr
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/02_step_01_move_execution.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/03_step_02_registry_alignment.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/04_step_03_active_docs_alignment.md
---

# Step 04 - prepare commits and PR

## Commit prepare A
Titre propose :
- `refactor(reseau_ssh): promote canonical module and archive legacy step1`

Scope :
- move top-level `reseau_ssh`
- archive `_archive/legacy_modules/reseau_ssh_step1`
- facade top-level `modules/reseau_ssh/scripts/*`

## Commit prepare B
Titre propose :
- `docs(registry): align reseau_ssh canonical naming and wrappers`

Scope :
- `registry/modules_registry.yaml`
- `registry/wrappers_registry.yaml`
- `docs/status/reseau_ssh_canonique.md`
- dossiers chantier `reseau_ssh`
- index de continuite utiles

## PR preparee
Titre propose :
- `[codex] refactor(reseau_ssh): promote canonical module and align registry`

Body propose :
- promotion repo-side du canonique `modules/reseau_ssh`
- archivage de l'ancien occupant `reseau_ssh_step1`
- realignement registre et docs
- aucun repointage machine-side des alias courts
- prochaine PR separee pour le runtime machine-side

## Regle
Commits et PR prepares seulement.

Aucune action Git n'est executee dans ce lot.

## Target
1 module canonique par famille.
