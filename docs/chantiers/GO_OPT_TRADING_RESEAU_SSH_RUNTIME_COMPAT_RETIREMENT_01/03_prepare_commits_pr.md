---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_PREPARE_GIT
doc_type: chantier_git_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01
status: open
lifecycle_stage: git_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - compat
  - git
  - pr
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/02_plan_operationnel_step_by_step.md
---

# Preparation commits et PR

## Commit recommande A

Titre propose :
- `docs(reseau_ssh): relaunch runtime compat retirement lot`

Scope :
- `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/*`
- readmes de statut `scripts/reseau_ssh/*`

## Commit recommande B

Titre propose :
- `fix(reseau_ssh): prevent legacy installer from republishing short aliases`

Scope :
- `scripts/reseau_ssh/install_reseau_ssh.sh`

## Commit recommande C

Titre propose :
- `chore(reseau_ssh): retire broken root wrappers`

Scope :
- `_archive/legacy_modules/reseau_ssh_root_wrappers_legacy/*`
- suppression active de :
  - `scripts/reseau_ssh_cmd.sh`
  - `scripts/reseau_ssh_menu.sh`

## PR recommandee

Titre propose :
- `[codex] reseau_ssh: start runtime compat retirement after canonical cutover`

Body attendu :
- contexte : alias courts deja repointes sur 4/4 hotes
- risque traite : republication legacy via `scripts/reseau_ssh/install_reseau_ssh.sh`
- nettoyage borne deja applique : wrappers racine historiques archives
- ce que la PR fait
- ce qu'elle ne fait pas
- prochaine etape : absorption ou depreciation du backend compat `scripts/reseau_ssh`, puis qualification de `reseau_ssh_step1b`

## Etat

Preparation uniquement.

Interdits a ce stade :
- aucun commit
- aucun push
- aucune PR

## Target
1 module canonique par famille.
