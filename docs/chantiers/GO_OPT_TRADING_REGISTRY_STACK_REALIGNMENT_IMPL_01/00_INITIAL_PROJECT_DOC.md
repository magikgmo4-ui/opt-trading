---
doc_id: GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01_INITIAL_PROJECT_DOC
doc_type: chantier_registry_realignement
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01
status: draft_for_review
lifecycle_stage: implementation
topic_keys:
  - opt-trading
  - registry
  - implementation
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01/40_ROLE_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01/50_REGISTRY_GAPS_AND_NEXT_ACTIONS.md
---

# 00_INITIAL_PROJECT_DOC

## Objet

Realigner `registry/modules_registry.yaml` avec la decision de stack registry posee par `GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01`.

## Modules traites

- `modules_registry_reader`
- `machines_registry_reader`
- `wrappers_registry_reader`
- `registry_meta_reader`
- `registry_router`
- `ui_registry_msi`

## Contraintes appliquees

- mutation limitee a `registry/modules_registry.yaml`
- aucun changement runtime
- aucun changement `wrappers_registry.yaml`
- aucun changement index global
- `secrets/` hors perimetre

## Verdict attendu

`PASS`
