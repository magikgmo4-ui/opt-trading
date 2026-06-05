---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_STEP_06_COMPAT_BACKEND_BLOCKER
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
  - backend
  - blocker
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/sanity_check.sh
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
  - scripts/reseau_ssh/sanity_reseau_ssh.sh
---

# Step 06 - blocage backend compat

## Constat

Le retrait des wrappers racine historiques est fait, mais `scripts/reseau_ssh` ne peut pas encore sortir du repo actif.

Motif :
- la façade canonique n'appelle plus `scripts/reseau_ssh`
- ce dossier reste seulement conserve pour rollback et appel legacy explicite

## Commandes encore presentes uniquement en legacy explicite

`scripts/reseau_ssh` porte encore en legacy explicite :
- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`
- `wg-server-init`
- `wg-client-init`
- `wg-add-peer`

## Decision

Etat exact de `scripts/reseau_ssh` :
- ni `archive_backup`
- classe retenue : `rollback_only`

## Prochaine etape

Avant tout archivage de `scripts/reseau_ssh`, il faut ouvrir un lot borne pour :
- qualifier si ce dossier doit rester en rollback local
- ou basculer en `archive_backup`
- sans rouvrir de dependance implicite depuis le canonique

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
