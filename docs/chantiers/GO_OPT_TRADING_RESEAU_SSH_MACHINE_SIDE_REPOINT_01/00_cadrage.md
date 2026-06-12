---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_CADRAGE
doc_type: chantier_child
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - reseau_ssh
  - machine
  - runtime
  - repoint
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md
  - modules/reseau_ssh/scripts/install_canonical_shortcuts.sh
  - modules/reseau_ssh/scripts/capture_shortcuts_snapshot.sh
  - scripts/reseau_ssh/install_reseau_ssh.sh
---

# GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01

## Objet
Preparer l'execution machine-side qui repointera les alias courts `reseau_ssh` vers le module canonique :
- `menu-reseau_ssh`
- `cmd-reseau_ssh`
- `sanity-reseau_ssh`

## Cible
Obtenir sur chaque machine Linux cible :
- alias courts pointant vers `modules/reseau_ssh/scripts/*`
- compat `*_reseau_ssh_step2` conservee pendant la transition
- rollback documente avant action

## Portee
- `db-layer`
- `admin-trading`
- `student`
- `fantome`

## Hors-scope
- retrait de `scripts/reseau_ssh`
- retrait de `step1b`
- retrait des alias `*_reseau_ssh_step2`
- execution distante dans ce lot
- execution Git

## Prerequis
L'execution reelle de ce lot demandera un acces SSH aux machines cibles.

Etat constate depuis la session courante :
- aliases SSH locaux resolves
- connectivite distante non prouvee depuis cette session
- timeouts observes vers les 4 machines

## Inventaire hostname retenu
- `db-layer`
- `admin-trading`
- `student`
- `fantome`

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
