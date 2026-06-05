---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01_STEP_04_PREPARE_GIT
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
  - commits
  - pr
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01/03_step_02_impl_facade.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01/04_step_03_validation_repo_side.md
---

# Step 04 - preparation commits et PR

## Commit prepare A
Titre propose :
- `feat(reseau_ssh): specialize canonical top-level facade`

Scope :
- `modules/reseau_ssh/scripts/_reseau_ssh_common.sh`
- `modules/reseau_ssh/scripts/cmd.sh`
- `modules/reseau_ssh/scripts/menu.sh`
- `modules/reseau_ssh/scripts/sanity_check.sh`

## Commit prepare B
Titre propose :
- `docs(reseau_ssh): align canonical facade documentation`

Scope :
- `modules/reseau_ssh/README.md`
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/README.md`
- `scripts/reseau_ssh/README.md`
- `scripts/reseau_ssh/README_RUNTIME_STATUS.md`
- dossier chantier courant

## PR preparee
Titre propose :
- `[codex] feat(reseau_ssh): specialize canonical facade before machine-side repoint`

Contenu :
- facade canonique repo-side
- delegation vers implementation interne
- compatibilites bornees
- aucun repointage machine-side

## Regle
Ces commits et cette PR sont prepares seulement.

Aucune action Git n'est executee dans ce lot.

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
