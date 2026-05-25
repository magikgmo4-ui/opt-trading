---
doc_id: GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01_APPLIED_REGISTRY_REALIGNMENT
doc_type: applied_change
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01
status: draft_for_review
lifecycle_stage: implementation
topic_keys:
  - opt-trading
  - registry
  - applied-change
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01/10_TARGET_REGISTRY_DELTA.md
---

# 20_APPLIED_REGISTRY_REALIGNMENT

## Fichier modifie

- `registry/modules_registry.yaml`

## Changements appliques

### Entrees ajoutees

- `modules_registry_reader`
- `machines_registry_reader`
- `wrappers_registry_reader`
- `registry_meta_reader`
- `registry_router`

### Entree requalifiee

- `ui_registry_msi`

## Metadata posees

- `domain: registry`
- `wrappers_expected: ["menu", "cmd", "sanity"]`
- descriptions explicites sur source de lecture ou facade
- dependances minimales pour `registry_router`

## Ce qui n'a pas ete change

- aucun script runtime
- aucun reader source file
- aucun `wrappers_registry.yaml`
- aucun `meta_index.yaml`
