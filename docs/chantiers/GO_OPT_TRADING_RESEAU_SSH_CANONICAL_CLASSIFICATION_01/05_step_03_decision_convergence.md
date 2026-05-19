---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01_STEP_03_CONVERGENCE
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - convergence
  - canonical
  - modules
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01/01_inventaire_et_classement_initial.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01/04_step_02_audit_blocage_runtime.md
  - docs/status/reseau_ssh_canonique.md
  - registry/wrappers_registry.yaml
---

# Step 03 - decision de convergence

## Decision
La famille converge vers :
- module canonique final : `modules/reseau_ssh`
- implementation interne : `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
- compat temporaire : `modules/reseau_ssh_step1b`
- compat runtime temporaire : `scripts/reseau_ssh`
- archive : `_archive/legacy_modules/reseau_ssh_step1`

## Etat d'execution
Cette decision n'est plus theorique.

Elle est deja executee repo-side pour :
- la recuperation du nom canonique `reseau_ssh`
- la sortie de l'ancien occupant legacy en archive
- la mise en place de la facade top-level

## Ce qui reste
- alignement final des docs et du registre repo-side
- repointage machine-side des alias courts
- retrait progressif des compatibilites

## Ce qui est refuse
- re-promouvoir `reseau_ssh_step2` comme nom canonique final
- garder durablement `scripts/reseau_ssh` comme publicateur officiel des alias courts
- archiver `step1b` avant decision d'absorption ou d'abandon de sa baseline utile

## Point de reprise
Le sous-lot utile suivant est :
- `GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01`

Puis :
- lot machine-side de repointage des alias courts

## Target
1 module canonique par famille.
