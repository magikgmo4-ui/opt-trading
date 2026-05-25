---
doc_id: GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01_TARGET_REGISTRY_DELTA
doc_type: registry_delta
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01
status: draft_for_review
lifecycle_stage: implementation
topic_keys:
  - opt-trading
  - registry
  - delta
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01/00_INITIAL_PROJECT_DOC.md
---

# 10_TARGET_REGISTRY_DELTA

## Ajouts

| Module | Role registry retenu |
| --- | --- |
| `modules_registry_reader` | owner canonique lecture `modules_registry.yaml` |
| `machines_registry_reader` | owner canonique lecture `machines_registry.yaml` |
| `wrappers_registry_reader` | owner canonique lecture `wrappers_registry.yaml` |
| `registry_meta_reader` | owner canonique lecture `meta_index.yaml` |
| `registry_router` | facade de navigation vers readers |

## Requalification

| Module | Ajustement |
| --- | --- |
| `ui_registry_msi` | description alignee sur son role de surface operateur active + owner de lecture UI |

## Machine target retenu

Pour les readers et le router, `machine_target: any` est retenu comme approximation minimale acceptable.

Raison:

- les README citent des cibles mixtes `admin-trading` et `msi_db_layer`
- le modele courant de `modules_registry.yaml` ne porte pas encore de cible multi-machine plus precise
