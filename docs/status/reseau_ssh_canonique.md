---
doc_id: OPT_TRADING_STATUS_RESEAU_SSH_CANONIQUE
doc_type: family_status
repo: opt-trading
project: opt-trading
module:
go_id:
status: validated
lifecycle_stage: consolidation
topic_keys:
  - opt-trading
  - status
  - reseau_ssh
  - module_family
  - runtime
search_tags:
  - surface:module_family
  - doc_role:carte
surface: module_family
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Reprise"
updated_at: 2026-04-25
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01/02_plan_operationnel_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/02_plan_operationnel_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md
---

# RESEAU_SSH — STATUT CANONIQUE

## Role documentaire
- role_actuel: fiche courte de statut de famille `reseau_ssh*`
- role_cible: fiche annexe de consolidation de lignee, non souveraine
- souverainete: ne remplace ni la matrice, ni les preuves runtime machine par machine, ni un arbitrage physique final

## ETABLI
- module canonique final retenu : `reseau_ssh`
- surface canonique repo-side en place : `modules/reseau_ssh`
- implementation interne utile : `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
- transition utile : `modules/reseau_ssh_step1b`
- ancien occupant top-level archive : `_archive/legacy_modules/reseau_ssh_step1`
- wrappers racine historiques archives : `_archive/legacy_modules/reseau_ssh_root_wrappers_legacy`
- registre repo-side aligne : `modules_registry` et `wrappers_registry`
- aliases courts machine-side repointes vers le canonique sur `db-layer`, `admin-trading`, `student`, `fantome`
- recroisement effectue avec `shared`, `shared_files_sftp`, `shared_sshfs_permanent`, `winscp_transfer`

## Survivant / Transition / Legacy / Archive
- survivant : `reseau_ssh`
- implementation interne : `reseau_ssh_step2`
- transition : `reseau_ssh_step1b`
- compat runtime : `scripts/reseau_ssh` reste encore present comme surface `rollback_only`, mais plus comme backend appele par la facade canonique ni comme point d'entree court sur les 4 machines ciblees
- archive : `_archive/legacy_modules/reseau_ssh_step1`, `_archive/legacy_modules/reseau_ssh_root_wrappers_legacy`

## Surfaces adjacentes
- `shared` : surface canonique inter-machines
- `shared_files_sftp` : exposition serveur SFTP de `shared`
- `shared_sshfs_permanent` : montage client Linux de `shared`
- `winscp_transfer` : workflow Windows / inbox-outbox sur la meme surface

## Reprise
- repo-side : `GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01`
- machine-side : `GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01`
- compat retirement : `GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01`
- absorption backend compat : `GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01`
- prochaine reduction ciblee : `GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01`, puis `reseau_ssh_step1b`

## Target
1 module canonique par famille.
