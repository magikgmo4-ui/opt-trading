---
doc_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01_PREPARE_GIT
doc_type: chantier_git_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01
status: open
lifecycle_stage: git_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - compat
  - git
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01/02_plan_operationnel_step_by_step.md
---

# Preparation commits et PR

## Commit recommande A

Titre propose :
- `docs(reseau_ssh): add compat backend absorption plan`

Scope :
- `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01/*`

## Commit recommande B

Titre propose :
- `refactor(reseau_ssh): cut deprecated wireguard compat delegation`

Scope potentiel :
- `modules/reseau_ssh/scripts/cmd.sh`
- eventuels README associes

## PR recommandee

Titre propose :
- `[codex] reseau_ssh: prepare compat backend absorption`

Body attendu :
- contexte : canonique en place, aliases courts migres, wrappers racine archives
- blocage restant : backend compat encore appele par la facade
- ce que la PR fait :
  - coupe `wg-server-init`, `wg-client-init`, `wg-add-peer` de la facade canonique
  - garde seulement `bootstrap`, `ssh-hardening-safe`, `ssh-lockdown` en transition
- ce qu'elle ne fait pas :
  - n'absorbe pas encore les trois commandes de transition restantes
  - n'archive pas encore `scripts/reseau_ssh`
- prochaine etape : retrait ou absorption des commandes `keep-transition`, puis requalification du backend compat

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
