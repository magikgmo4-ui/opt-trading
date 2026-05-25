---
doc_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01_RUNTIME_SURFACE_MAP
doc_type: runtime_surface_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - registry
  - runtime
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01/20_CALLERS_AUDIT.md
---

# 30_RUNTIME_SURFACE_MAP

## Logical map

```text
registry/meta_index.yaml
  -> registry_meta_reader
  -> points to primary consumers

registry/modules_registry.yaml
  -> modules_registry_reader

registry/machines_registry.yaml
  -> machines_registry_reader

registry/wrappers_registry.yaml
  -> wrappers_registry_reader

registry/ui_surfaces_registry.yaml
  -> ui_registry_msi
  -> exports JSON/MD views

registry_router
  -> navigation facade to meta/machines/modules/ui/wrappers readers
```

## Role map

| Role | Surface | Classement |
| --- | --- | --- |
| source de verite modules | `registry/modules_registry.yaml` | canon source |
| source de verite machines | `registry/machines_registry.yaml` | canon source |
| source de verite wrappers | `registry/wrappers_registry.yaml` | canon source |
| source de verite UI | `registry/ui_surfaces_registry.yaml` | canon source |
| source de verite meta | `registry/meta_index.yaml` | canon source meta |
| owner lecture modules | `modules_registry_reader` | reader specialise |
| owner lecture machines | `machines_registry_reader` | reader specialise |
| owner lecture wrappers | `wrappers_registry_reader` | reader specialise |
| owner lecture meta | `registry_meta_reader` | meta-reader specialise |
| owner lecture/export UI | `ui_registry_msi` | UI registry active |
| facade de navigation | `registry_router` | facade complementaire |

## Runtime classification

| Surface | Classification |
| --- | --- |
| readers specialises | runtime utilitaire read-only |
| `registry_meta_reader` | runtime utilitaire read-only |
| `ui_registry_msi` | surface operateur complementaire active |
| `registry_router` | facade utilitaire active |
