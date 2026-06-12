---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01_STEP_02_REGISTRY
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - registry
  - wrappers
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - registry/modules_registry.yaml
  - registry/wrappers_registry.yaml
---

# Step 02 - registry alignment

## Modules registry
`registry/modules_registry.yaml` porte maintenant :
- `module_name: reseau_ssh`
- statut `active`
- wrappers attendus `cmd`, `menu`, `sanity`

## Wrappers registry
`registry/wrappers_registry.yaml` porte maintenant :
- `cmd/menu/sanity-reseau_ssh`
- `cmd/menu/sanity-reseau_ssh_step2`

## Lecture correcte
- `reseau_ssh` = wrappers canoniques finaux
- `reseau_ssh_step2` = wrappers suffixes de compat transitoire

## Limite maintenue
Le registre est aligne cote repo.

Il ne prouve pas encore le repointage machine-side reel.

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
