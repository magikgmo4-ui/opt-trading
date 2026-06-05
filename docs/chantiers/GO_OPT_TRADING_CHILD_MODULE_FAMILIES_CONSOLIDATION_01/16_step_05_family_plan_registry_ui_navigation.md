---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_05_REGISTRY_UI_NAV
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-05
  - registry
  - ui
  - navigation
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md
  - registry/README.md
  - registry/ui_surfaces_registry.yaml
  - registry/wrappers_registry.yaml
  - docs/ui_indexation/01_ui_registry_modules.md
  - docs/ui_indexation/02_ui_registry_wrappers.md
  - modules/registry_router/README.md
  - modules/machines_registry_reader/README.md
  - modules/modules_registry_reader/README.md
  - modules/registry_meta_reader/README.md
  - modules/wrappers_registry_reader/README.md
  - modules/ui_registry_msi/README.md
  - modules/ops_menu_hub/README.md
  - modules/ops_super_menu/README.md
  - modules/ops_wrappers/README.md
---

# Step 05 - family plan `Registry/UI/navigation`

## Statut
Complete.

## Objet
Fixer la structuration P2 de la suite `Registry/UI/navigation`, en distinguant source de verite declarative, lecture outillee, hub operateur, couche d'index UI et consumer externe eventuel.

## Verifications utilisees
- lecture de `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md`
- lecture de `registry/README.md`
- lecture de `registry/ui_surfaces_registry.yaml`
- lecture de `registry/wrappers_registry.yaml`
- lecture de `docs/ui_indexation/01_ui_registry_modules.md`
- lecture de `docs/ui_indexation/02_ui_registry_wrappers.md`
- lecture des README de :
  - `modules/registry_router`
  - `modules/machines_registry_reader`
  - `modules/modules_registry_reader`
  - `modules/registry_meta_reader`
  - `modules/wrappers_registry_reader`
  - `modules/ui_registry_msi`
  - `modules/ops_menu_hub`
  - `modules/ops_super_menu`
  - `modules/ops_wrappers`

## Carte de suite
| Couche | Surface retenue | Role |
|---|---|---|
| source de verite declarative | `registry/` | YAML canoniques machines / modules / UI / wrappers |
| lecture read-only | `machines_registry_reader`, `modules_registry_reader`, `registry_meta_reader`, `wrappers_registry_reader` | lectures ciblees des registres |
| routage de lecture | `registry_router` | point d'entree unique vers les readers |
| index UI cote producer | `ui_registry_msi` | vue structuree des surfaces UI repo-sources |
| navigation operateur CLI | `ops_menu_hub` | hub d'usage quotidien pour l'operateur |
| inventaire / secours wrappers | `ops_super_menu`, `ops_wrappers` | outillage d'inventaire et de fallback |
| consumer UI externe eventuel | `localcms` | consumer hors repo, non absorbable dans ce lot |

## Frontieres retenues
- `registry/` reste la source de verite declarative. Aucun module `*_reader`, `registry_router` ou `ui_registry_msi` ne doit la remplacer.
- `registry_router` reste un routeur de lecture. Il ne devient ni hub operateur generaliste, ni UI productisee.
- `ui_registry_msi` reste un index UI cote producer `opt-trading`, branche sur `registry/ui_surfaces_registry.yaml`.
- `ops_menu_hub` reste le hub CLI operateur. Il ne doit pas etre confondu avec un registre ni avec une UI consumer.
- `ops_super_menu` et `ops_wrappers` restent des outils d'inventaire / fallback, pas des sources canoniques.
- `localcms` reste un consumer UI externe eventuel :
  - `opt-trading` reste producer canonique
  - `localcms` ne doit pas etre traite comme module de cette famille

## Ce qui doit etre harmonise
- terminologie commune entre `registry_router`, readers et `ui_registry_msi`
- conventions d'entrees `status`, `list`, `show-*`, `export-*`
- cross-links entre registres, readers et index UI
- matrice producer / consumer pour les UI partageables vers `localcms`

## Ce qui peut etre mutualise plus tard
- bibliotheque de lecture YAML commune entre readers si la duplication technique est reelle
- conventions de rendu/export pour `ui_registry_msi` et readers
- eventuelle couche d'adaptateurs d'exposition UI pour `localcms`

## Ce qui doit rester separe
- `registry/` et la logique de navigation operateur
- `ui_registry_msi` et le consumer `localcms`
- `ops_menu_hub` et `registry_router`
- `ops_super_menu` / `ops_wrappers` et la source de verite wrappers

## Risques a eviter
- promouvoir `ui_registry_msi` comme source de verite a la place de `registry/`
- rabattre `ops_menu_hub` dans `registry_router` et perdre la frontiere entre lecture declarative et hub operateur
- demarrer une migration UI vers `localcms` sans matrice producer/consumer ni contrat d'exposition
- traiter les outils d'inventaire `ops_super_menu` / `ops_wrappers` comme canon fonctionnel

## Decision retenue
- oui a une suite P2 coherente `Registry/UI/navigation`
- non a une fusion de modules dans ce lot
- `localcms` est integre au raisonnement comme consumer UI externe eventuel, pas comme surface a deplacer dans `opt-trading`
- prochain sous-lot logique si besoin :
  - inventory producer/consumer
  - contracts d'exposition UI vers `localcms`

## Rollback
- revert doc-only de cette note
- revert doc-only du plan si besoin

## Point de reprise
Suite P2 `Registry/UI/navigation` cadree. Basculer sur `Openclaw`, `Collectors / market intelligence` et `Vision`.

## RISKS

- À qualifier.
