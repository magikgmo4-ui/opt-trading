---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01_CADRAGE
doc_type: chantier_child
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - reseau_ssh
  - canonical
  - rename
  - registry
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01/02_plan_operationnel_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/02_plan_operationnel_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01/01_plan_operationnel_step_by_step.md
  - docs/status/reseau_ssh_canonique.md
  - registry/modules_registry.yaml
  - registry/wrappers_registry.yaml
---

# GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01

## Objet
Tracer le lot repo-side qui :
- documente la liberation du nom canonique
- documente la promotion de l'ancienne base `step2`
- aligne le registre et les docs actives
- prepare commits et PR sans execution Git

## Portee
- move top-level deja execute
- registre `modules` et `wrappers`
- docs actives `reseau_ssh`
- index/statuts de continuite utiles

## Hors-scope
- repointage machine-side des alias courts
- retrait de `step1b`
- retrait de `scripts/reseau_ssh`
- execution Git

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
