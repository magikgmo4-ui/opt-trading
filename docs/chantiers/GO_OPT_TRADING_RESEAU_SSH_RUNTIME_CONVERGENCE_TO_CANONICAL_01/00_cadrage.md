---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01_CADRAGE
doc_type: chantier_child
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - reseau_ssh
  - runtime
  - convergence
  - canonical
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01/05_step_03_decision_convergence.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01/01_plan_operationnel_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md
  - scripts/reseau_ssh/README_RUNTIME_STATUS.md
  - modules/reseau_ssh/README.md
---

# GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01

## Objet
Preparer la convergence runtime de la famille `reseau_ssh` vers son canonique unique.

## Cible
Faire en sorte que la surface operateur finale :
- `menu-reseau_ssh`
- `cmd-reseau_ssh`
- `sanity-reseau_ssh`

soit publiee depuis :
- `modules/reseau_ssh`

## Etat courant
- `modules/reseau_ssh` = canonique repo-side
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2` = implementation interne
- `modules/reseau_ssh_step1b` = compat temporaire baseline
- `scripts/reseau_ssh` = publicateur machine-side actuel des alias courts

## Anti-cibles
- pas de retour a `reseau_ssh_step2` comme nom canonique final
- pas de repointage machine-side dans ce lot documentaire
- pas d'archivage de `step1b` avant arbitrage de sa baseline utile

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
