---
doc_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01_STACK_INVENTORY
doc_type: stack_inventory
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - registry
  - stack
  - inventory
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01/00_INITIAL_PROJECT_DOC.md
---

# 10_STACK_INVENTORY

## Inventory snapshot

| Surface | Role constate | Statut retenu |
| --- | --- | --- |
| `registry/modules_registry.yaml` | source de verite modules | canon source |
| `registry/machines_registry.yaml` | source de verite machines | canon source |
| `registry/wrappers_registry.yaml` | source de verite wrappers | canon source |
| `registry/meta_index.yaml` | index meta des registries | canon source meta |
| `registry/ui_surfaces_registry.yaml` | source de verite UI surfaces | canon source UI |
| `modules/modules_registry_reader` | reader specialise modules | owner canonique lecture modules |
| `modules/machines_registry_reader` | reader specialise machines | owner canonique lecture machines |
| `modules/wrappers_registry_reader` | reader specialise wrappers | owner canonique lecture wrappers |
| `modules/registry_meta_reader` | reader de `meta_index.yaml` | owner canonique meta-reader |
| `modules/ui_registry_msi` | reader + export UI surfaces | surface operateur complementaire + owner lecture UI |
| `modules/registry_router` | facade de navigation vers readers | facade/router utile |

## File-to-reader ownership

| File | Primary consumer declare | Owner retenu |
| --- | --- | --- |
| `registry/modules_registry.yaml` | `modules/modules_registry_reader` | `modules_registry_reader` |
| `registry/machines_registry.yaml` | `modules/machines_registry_reader` | `machines_registry_reader` |
| `registry/wrappers_registry.yaml` | `modules/wrappers_registry_reader` | `wrappers_registry_reader` |
| `registry/meta_index.yaml` | `modules/registry_meta_reader` | `registry_meta_reader` |
| `registry/ui_surfaces_registry.yaml` | `modules/ui_registry_msi` | `ui_registry_msi` |

## Module notes

### `modules_registry_reader`

- lit `registry/modules_registry.yaml`
- groupe par domaine, exporte JSON, montre un module cible
- role clair et specialise

### `machines_registry_reader`

- lit `registry/machines_registry.yaml`
- groupe par role machine, exporte JSON
- role clair et specialise

### `wrappers_registry_reader`

- lit `registry/wrappers_registry.yaml`
- groupe par famille de wrappers, exporte JSON
- role clair et specialise

### `registry_meta_reader`

- lit `registry/meta_index.yaml`
- decrit quels registries existent et qui les consomme
- fonctionne comme index meta, pas comme reader substitut des registries cibles

### `ui_registry_msi`

- lit prioritairement `registry/ui_surfaces_registry.yaml`
- fallback local possible via `config/ui_registry_seed.json`
- exporte JSON/MD et offre des vues par machine/categorie
- surface registry/UI active, pas dashboard metier final

### `registry_router`

- ne lit aucun fichier registry directement
- expose seulement des entrees de navigation vers readers et `ui_registry_msi`
- facade de routage, pas source de verite ni owner de lecture

## Nature de la stack

La stack registry est une **stack complementaire** :

- des fichiers sources de verite
- des readers specialises par source
- un meta-reader d'index
- une UI/operateur specialisee pour les surfaces UI
- une facade de routage pour l'exploration rapide
