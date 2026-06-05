---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_STEP_05_ROOT_WRAPPERS_EXEC
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - compat
  - wrappers
  - archive
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/04_step_03_audit_wrappers_racine.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/05_step_04_arbitrage_sortie.md
  - _archive/legacy_modules/reseau_ssh_root_wrappers_legacy/README.md
---

# Step 05 - execution wrappers racine

## Action appliquee

Les deux wrappers racine historiques ont ete retires du flux actif et deplaces vers :
- `_archive/legacy_modules/reseau_ssh_root_wrappers_legacy/reseau_ssh_cmd.sh`
- `_archive/legacy_modules/reseau_ssh_root_wrappers_legacy/reseau_ssh_menu.sh`

## Motif d'execution

Conditions remplies :
- aucun caller repo-side critique explicite prouve
- implementation locale cassée dans le repo courant
- aucun role canonique
- aliases courts machine-side deja repointes vers `modules/reseau_ssh/scripts/*`

## Effet

- les wrappers racine ne peuvent plus etre confondus avec des surfaces actives
- le flux actif `reseau_ssh` est recentre sur :
  - `modules/reseau_ssh`
  - `scripts/reseau_ssh` comme `compat_active_backend`
  - `modules/reseau_ssh_step1b` comme transition encore qualifiee a part

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
