---
go_id: GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01
doc_type: REGISTRY_SOURCE_MAP
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 10_REGISTRY_SOURCE_MAP

## Decision

Oui: `registry/*.yaml` reste prioritaire sur tout fallback local.

## Sources centrales de verite

| Registry | Source centrale | Reader proprietaire | Role |
| --- | --- | --- | --- |
| modules | `registry/modules_registry.yaml` | `modules/modules_registry_reader` | catalogue canonique des modules |
| machines | `registry/machines_registry.yaml` | `modules/machines_registry_reader` | catalogue canonique des machines |
| wrappers | `registry/wrappers_registry.yaml` | `modules/wrappers_registry_reader` | catalogue canonique des wrappers |
| ui | `registry/ui_surfaces_registry.yaml` | `modules/ui_registry_msi` | catalogue canonique des surfaces UI |
| meta | `registry/meta_index.yaml` | `modules/registry_meta_reader` | index canonique des registres centraux |

## Readers et surfaces non-sources

- `registry_router` = facade de navigation, jamais source de verite
- `modules/*_registry_reader/output/*.json` = exports derives, jamais sources
- `modules/install_module_openclaw/app/modules_registry.json` = copie locale specialisee, jamais source centrale
- `modules/ui_registry_msi/config/ui_registry_seed.json` = seed local de secours, jamais source centrale

## Rule

Le contrat canonique devient:

1. verite centrale = `registry/*.yaml`
2. lecture canonique = readers specialises
3. navigation = facade/router
4. export, seed, copie locale = derives ou fallbacks, jamais autorite
