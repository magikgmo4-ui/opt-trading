---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
BUNDLE_TARGET: RUNTIME_ACCESS_OPTIMIZATION_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
TRANSPORT_MODE: patch_only
6_FINAL_TARGET: Optimiser l'acces runtime aux inventaires pro_desk_data_inventory.json et source_candidates.json, en separant source canonique, index compiles, cache memoire, source selector et views Data Center, pour eviter un goulot d'etranglement entre producers et consumers.
topic_keys:
  - opt-trading
  - data_center
  - runtime_optimization
  - inventory_access
  - source_selector
  - hot_path
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/99_PARENT_CLOSE_GATE.md
  - modules/data_center/registry/pro_desk_data_inventory.json
  - modules/data_center/registry/source_candidates.json
  - modules/data_center/registry/producers.json
  - modules/data_center/registry/consumers.json
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01

## Objet

Les inventaires `pro_desk_data_inventory.json` (~500 champs) et `source_candidates.json` (31 sources candidates) sont des fichiers plats. A chaque requete d'un consumer (DeskPro, Strategy, Perf), si le Data Center lit ces fichiers en entier, cela devient un goulot.

Ce child specifie l'architecture d'acces runtime : compilation d'index, cache memoire, separation hot/cold path, source selector, et vues Data Center optimisees.

## 1_MASTER_TARGET

*(herite du parent)* Data Center = stockage + transit + normalisation + scoring source + arbitrage source candidate. Consumer = utilise la donnee exposee, ne choisit pas les sources brutes.

Objectif immediat : garantir que l'acces aux inventaires P0-P21 et aux sources candidates ne freine pas les consumers en production.

## 3_INITIAL_NEED

```text
pro_desk_data_inventory.json = ~500 champs, ~150 KB
source_candidates.json = 31 sources, ~30 KB

A chaque requete consumer :
- si lecture brute → 150 KB parse JSON par appel
- si 10 consumers × 10 symboles × 6 data_keys = 600 appels → ~90 MB parse
- solution : index compiles + cache memoire + vues pre-calculees
```

## 4_MASTER_PROJECT_PLAN

1. `10_RUNTIME_ACCESS_PROBLEM.md` — diagnostiquer le probleme d'acces runtime.
2. `20_HOT_PATH_AND_COLD_PATH_DESIGN.md` — separer les chemins chauds (lus a chaque requete) et froids (lus rarement).
3. `30_COMPILED_INDEXES_PLAN.md` — specifier les index compiles.
4. `40_SOURCE_SELECTION_POLICY.md` — formaliser la policy de selection de source.
5. `50_PERFORMANCE_BENCHMARK_PLAN.md` — definir les benchmarks.
6. `60_LANGUAGE_AND_STORAGE_DECISION.md` — choisir format de stockage runtime.

## 6_FINAL_TARGET

```text
RUNTIME_ACCESS_OPTIMIZATION_V1
```

## 11_KEY_DECISIONS

- L'inventaire canonique (`pro_desk_data_inventory.json`) est la source of truth, jamais modifie par le runtime.
- Les index compiles sont regeneres a chaque modification de l'inventaire, pas a chaque requete.
- Le hot path ne lit jamais le JSON brut.
- Le source selector utilise les index compiles, pas le fichier source.
- Les views Data Center sont pre-calculees pour les consumers.

## 12_INVARIANTS

- Ne pas modifier les index globaux.
- Aucune modification runtime (readers, producers, resolvers).
- Aucun appel API, DB, Telegram.
- `pro_desk_data_inventory.json` et `source_candidates.json` restent les sources canoniques (ajout registries, pas modification de registries existants).
- Data Center arbitre les sources, ne decide pas les trades.

## 16_TODO

Produire les 7 livrables (10_ a 60_ + 90_).

## 17_RESUME_POINT

Reprendre ici : child optimisation ouvert. Livrables a produire dans l'ordre.
