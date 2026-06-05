---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_STEP_03_ROOT_WRAPPERS
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
  - legacy
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/02_plan_operationnel_step_by_step.md
  - scripts/reseau_ssh_cmd.sh
  - scripts/reseau_ssh_menu.sh
---

# Step 03 - audit des wrappers racine

## Surfaces auditees
- `scripts/reseau_ssh_cmd.sh`
- `scripts/reseau_ssh_menu.sh`

## Constat technique

Les deux wrappers racine existent encore, mais leur implementation locale pointe vers des chemins absents dans le repo courant :
- `scripts/apply_linux.sh`
- `scripts/apply_hostname_linux.sh`
- `templates/hosts.block`
- `templates/ssh_config.linux`

Conclusion :
- les wrappers racine sont localement non fonctionnels dans l'etat courant du repo

## Audit de references

Resultat observe :
- aucun caller repo-side critique explicite n'a ete trouve vers le chemin exact `scripts/reseau_ssh_cmd.sh`
- aucun caller repo-side critique explicite n'a ete trouve vers le chemin exact `scripts/reseau_ssh_menu.sh`
- les references observees restantes sont principalement :
  - les fichiers eux-memes
  - des scripts internes a d'autres variantes `reseau_ssh`
  - de la documentation historique

## Classe retenue

Les deux wrappers racine sont reclasses :
- `legacy_fige_broken`

Ils ne sont plus des surfaces actives a conserver comme entree utilisateur.

## Decision de cette passe

Pas de retrait physique dans cette passe.

Le retrait ou l'archivage de ces deux wrappers est maintenant :
- techniquement defendable
- mais reporte a un lot Git separe et borne

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
