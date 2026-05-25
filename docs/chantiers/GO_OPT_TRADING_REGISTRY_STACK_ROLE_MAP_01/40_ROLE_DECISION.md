---
doc_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01_ROLE_DECISION
doc_type: role_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - registry
  - role-decision
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01/30_RUNTIME_SURFACE_MAP.md
---

# 40_ROLE_DECISION

## Reponses tranchees

### 1. Owner canonique lecture modules

- `modules/modules_registry_reader`

### 2. Owner canonique lecture machines

- `modules/machines_registry_reader`

### 3. Owner canonique lecture wrappers

- `modules/wrappers_registry_reader`

### 4. `registry_router`

Verdict: **facade utile**, pas legacy, pas source de verite, pas reader concurrent.

### 5. `ui_registry_msi`

Verdict: **surface operateur complementaire active** et owner canonique de la lecture `ui_surfaces_registry`.

### 6. Doublon readers vs router

Verdict: **non**, sauf ambiguite de vocabulaire.

Le router ne lit pas; il oriente.

### 7. Nature globale de la stack registry

Verdict: **stack complementaire par couches**, composee de :

- fichiers sources de verite
- readers specialises par source
- meta-reader d'index
- UI registry active
- facade de routage

## Classement final

| Surface | Classement |
| --- | --- |
| `registry/modules_registry.yaml` | source de verite modules |
| `registry/machines_registry.yaml` | source de verite machines |
| `registry/wrappers_registry.yaml` | source de verite wrappers |
| `registry/ui_surfaces_registry.yaml` | source de verite UI |
| `registry/meta_index.yaml` | source de verite meta |
| `modules_registry_reader` | owner canonique lecture modules |
| `machines_registry_reader` | owner canonique lecture machines |
| `wrappers_registry_reader` | owner canonique lecture wrappers |
| `registry_meta_reader` | owner canonique lecture meta |
| `ui_registry_msi` | UI/operator registry active |
| `registry_router` | facade utilitaire de navigation |

## Verdict

**PASS**

La stack registry est clarifiee sans mutation runtime ni registry.
