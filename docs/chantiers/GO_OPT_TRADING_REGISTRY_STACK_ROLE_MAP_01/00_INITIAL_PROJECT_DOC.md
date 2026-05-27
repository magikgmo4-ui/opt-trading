---
doc_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01_INITIAL_PROJECT_DOC
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - registry
  - stack
  - role-map
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01/40_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv
  - registry/meta_index.yaml
---

# 00_INITIAL_PROJECT_DOC

## Objet

Cartographier la stack registry du repo pour distinguer clairement :

- les sources de verite par fichier registry
- les readers specialises
- le meta-reader
- le router
- la surface UI / operateur
- les gaps transverses encore ouverts apres P1 et les realignements `desk` / `openclaw`

## Stack cible

- `modules/modules_registry_reader`
- `modules/machines_registry_reader`
- `modules/wrappers_registry_reader`
- `modules/registry_meta_reader`
- `modules/registry_router`
- `modules/ui_registry_msi`
- `registry/modules_registry.yaml`
- `registry/machines_registry.yaml`
- `registry/wrappers_registry.yaml`
- `registry/meta_index.yaml`
- `registry/ui_surfaces_registry.yaml`

## Etat d'entree

- `sot/mainline` alignee avec `origin/sot/mainline`
- `secrets/` non suivi et hors perimetre
- `registry/modules_registry.yaml` vient d'etre enrichi pour `desk` puis `openclaw`
- aucun runtime ne doit etre modifie dans ce GO

## Questions a trancher

1. Quel module est owner canonique de la lecture `modules_registry` ?
2. Quel module est owner canonique de la lecture `machines_registry` ?
3. Quel module est owner canonique de la lecture `wrappers_registry` ?
4. `registry_router` est-il runtime utile, facade, ou legacy ?
5. `ui_registry_msi` est-il UI active, legacy, ou surface operateur complementaire ?
6. Y a-t-il doublon entre readers et router ?
7. Quels gaps registry restent apres P1 + OpenClaw ?
8. Quel GO suivant doit traiter les mutations registry transverses ?

## Contraintes appliquees

- mode `doc-only`
- aucun runtime
- aucune mutation registry dans ce GO
- aucun index global ajoute
- aucun toucher a `secrets/`
- machine_owner: lecture mixte `admin-trading` + `msi_db_layer`, pas d'unique owner machine
