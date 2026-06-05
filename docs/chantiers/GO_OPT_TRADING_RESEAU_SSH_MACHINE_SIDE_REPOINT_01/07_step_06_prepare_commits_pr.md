---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_STEP_06_PREPARE_GIT
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - machine
  - commits
  - pr
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/install_canonical_shortcuts.sh
  - modules/reseau_ssh/scripts/capture_shortcuts_snapshot.sh
---

# Step 06 - prepare commits and PR

## Commit prepare A
Titre propose :
- `feat(reseau_ssh): add machine-side canonical shortcut helpers`

Scope :
- `modules/reseau_ssh/scripts/install_canonical_shortcuts.sh`
- `modules/reseau_ssh/scripts/capture_shortcuts_snapshot.sh`
- `modules/reseau_ssh/README.md`

## Commit prepare B
Titre propose :
- `docs(reseau_ssh): add machine-side repoint runbooks`

Scope :
- dossier chantier `GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01`
- éventuellement mise à jour de `docs/status/reseau_ssh_canonique.md` après exécution réelle

## PR preparee
Titre propose :
- `[codex] feat(reseau_ssh): prepare machine-side canonical shortcut repoint`

Contenu :
- helpers non destructifs
- runbooks par machine
- aucun accès distant exécuté
- aucun repointage machine lancé depuis la PR

## Regle
Commits et PR préparés seulement.

Aucune action Git n'est exécutée dans ce lot.

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
