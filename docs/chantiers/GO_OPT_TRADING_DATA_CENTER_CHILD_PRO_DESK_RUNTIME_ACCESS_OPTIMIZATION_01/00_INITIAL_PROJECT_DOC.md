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

1. `10_RESEARCH_FINDINGS_MULTI_SOURCE_DATA_CENTER.md` — etat de l'art multi-source, MDM, data contracts, lineage.
2. `20_CURRENT_RUNTIME_RISK_ANALYSIS.md` — diagnostiquer le probleme d'acces runtime + analyse de risques R01-R10.
3. `30_HOT_PATH_COLD_PATH_ARCHITECTURE.md` — separer les chemins chauds et froids, diagramme ASCII du pipeline.
4. `40_COMPILED_INDEXES_AND_CACHE_PLAN.md` — specifier les 5 index compiles + schemas JSON concrets + cache snapshot.
5. `50_SOURCE_SELECTION_POLICY_PROFILES.md` — 4 modes de selection (best, all, consensus, fallback).
6. `60_LANGUAGE_STORAGE_AND_SQLITE_DECISION.md` — matrice 6 formats + option SQLite benchmark.
7. `70_BENCHMARK_AND_ACCEPTANCE_CRITERIA.md` — B01-B08 benchmarks + criteres go/no-go AC01-AC14 + NG01-NG08.

## 6_FINAL_TARGET

```text
RUNTIME_ACCESS_OPTIMIZATION_V1
```

## 11_KEY_DECISIONS

- JSON canonique reste source of truth.
- Hot path ne doit pas scanner les JSON complets.
- Compiled indexes + cache snapshot = solution V1 par defaut.
- SQLite WAL = option a benchmarker, pas obligation immediate.
- Data Center arbitre la source.
- Consumers decident l'usage.
- Toutes les candidates sont preservees.
- Toute selection doit avoir policy + trace.
- Python dict / JSON indexe = choix V1 par defaut tant que benchmarks tiennent.
- Toutes les performances sont TARGET/ESTIMATE tant que B01-B08 non executes.

## 12_INVARIANTS

- Ne pas modifier les index globaux.
- Aucun reader / producer / resolver runtime modifie.
- Aucun reader consumer cree.
- Aucun producer path lu directement par consumer.
- Pas de decision trading dans Data Center.
- Data Center arbitre les sources, ne decide pas les trades.
- `pro_desk_data_inventory.json` et `source_candidates.json` restent les sources canoniques (ajout registries, pas modification de registries existants).

## 16_TODO

Produire les 8 livrables (10_ a 70_ + 90_) — fusion des specs RUNTIME_ACCESS_OPTIMIZATION + RUNTIME_SOURCE_SELECTION_OPTIMIZATION.

## 17_RESUME_POINT

Reprendre ici : child optimisation ouvert avec structure canonique 9 fichiers. NEXT_GO = `GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_INDEX_IMPLEMENTATION_01`.
