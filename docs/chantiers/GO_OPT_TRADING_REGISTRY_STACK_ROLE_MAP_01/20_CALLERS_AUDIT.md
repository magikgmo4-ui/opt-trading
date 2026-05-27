---
doc_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01_CALLERS_AUDIT
doc_type: callers_audit
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - registry
  - callers
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01/10_STACK_INVENTORY.md
---

# 20_CALLERS_AUDIT

## Direct callers and declarations

| Surface | Caller / declaration | Lecture |
| --- | --- | --- |
| `modules_registry_reader` | `registry/meta_index.yaml` primary consumer | owner canonique lecture modules |
| `machines_registry_reader` | `registry/meta_index.yaml` primary consumer | owner canonique lecture machines |
| `wrappers_registry_reader` | `registry/meta_index.yaml` primary consumer | owner canonique lecture wrappers |
| `ui_registry_msi` | `registry/meta_index.yaml` primary consumer for `ui_surfaces_registry` | owner canonique lecture UI |
| `registry_router` | `scripts/ai/menu/opt_trading_menu.json`; README propre | facade de navigation exposee |

## Cross-calls inside stack

| Surface | Evidence | Lecture |
| --- | --- | --- |
| `registry_router` | liste `meta`, `machines`, `modules`, `ui`, `wrappers` dans `entries` | depend des readers, ne les remplace pas |
| `ui_registry_msi` | lit `registry/ui_surfaces_registry.yaml` puis fallback local | UI active avec source centrale prioritaire |
| `registry_meta_reader` | expose les `primary_consumer` des registries | couche meta d'orientation |

## UI / operator exposure

| Surface | Exposure | Lecture |
| --- | --- | --- |
| `ui_registry_msi` | deja present dans `modules_registry.yaml` et `opt_trading_menu.json` | surface operateur active |
| `registry_router` | present dans `opt_trading_menu.json` | facade utile pour navigation |

## Duplicate risk assessment

Le seul risque de doublon est conceptuel, pas fonctionnel.

- les readers lisent les sources de verite
- `registry_router` ne fait que pointer vers eux
- `registry_meta_reader` ne lit pas les memes fichiers qu'eux; il lit l'index des registries
- `ui_registry_msi` est specialise sur `ui_surfaces_registry`, avec export et vues operateur

Conclusion:

- pas de doublon d'implementation majeur entre readers et router
- mais vocabulaire potentiellement trompeur si `registry_router` etait decrit comme un reader ou une source de verite
