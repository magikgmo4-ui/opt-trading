---
doc_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01_PREPARE_GIT
doc_type: chantier_git_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01
status: open
lifecycle_stage: git_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - transition
  - git
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01/02_plan_operationnel_step_by_step.md
---

# Preparation commits et PR

## Commit recommande A

Titre propose :
- `docs(reseau_ssh): define transition command absorption plan`

Scope :
- `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01/*`

## Commit recommande B

Titre propose :
- `refactor(reseau_ssh): absorb transition ssh bootstrap commands`

Scope potentiel :
- `modules/reseau_ssh/scripts/cmd.sh`
- `modules/reseau_ssh/scripts/menu.sh`
- nouveaux helpers shell canoniques eventuels
- `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01/*`
- `scripts/reseau_ssh/README.md`
- `scripts/reseau_ssh/README_RUNTIME_STATUS.md`
- `docs/status/reseau_ssh_canonique.md`

## PR recommandee

Titre propose :
- `[codex] reseau_ssh: absorb remaining transition commands`

Body attendu :
- contexte : module canonique publie, commandes WireGuard legacy retirees de la facade
- blocage restant initial : trois commandes de transition encore implementees hors canonique
- ce que la PR fait :
  - absorbe `bootstrap`, `ssh-hardening-safe`, `ssh-lockdown` dans `modules/reseau_ssh`
  - coupe la derniere delegation implicite via `menu.sh`
  - requalifie `scripts/reseau_ssh` en `rollback_only`
- ce qu'elle ne fait pas :
  - n'archive pas encore `scripts/reseau_ssh`
  - ne retire pas encore `reseau_ssh_step1b`
- prochaine etape : arbitrage final `rollback_only` -> `archive_backup`

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
