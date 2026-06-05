---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01_BENCHMARK_AND_ACCEPTANCE_CRITERIA
doc_type: acceptance_criteria
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 70_BENCHMARK_AND_ACCEPTANCE_CRITERIA

## Objectif

Definir les benchmarks avant implementation runtime.

## Benchmarks requis

| Benchmark | Cible V1 |
|---|---|
| cold load canonical registries | mesure obligatoire |
| compile indexes duration | mesure obligatoire |
| warm lookup by data_key | cible < 5 ms |
| warm lookup candidates by data_key | cible < 5 ms |
| source selection p95 hors I/O producer | cible < 20 ms |
| snapshot reload time | mesure obligatoire |
| memory footprint snapshot | mesure obligatoire |
| SQLite lookup option | comparer a compiled JSON |
| invalid registry handling | fail closed avec message clair |
| missing compiled indexes | fallback controle ou rebuild |

## Scenarios a tester

```text
small_fixture
medium_fixture
large_fixture
missing_source
stale_source
conflicting_sources
many_candidates_one_data_key
many_consumers_same_data_key
registry_checksum_change
compiled_index_missing
```

## Acceptance criteria

Le child implementation futur peut passer si :

- aucun full scan dans le hot path normal ;
- toutes les candidates sont preservees ;
- chaque selection a une policy et une trace ;
- lookup p95 respecte la cible sur fixture medium ;
- fallback si compiled indexes absents est explicite ;
- atomic write documente et teste ;
- aucun consumer ne lit les producer paths directement ;
- aucun usage trading n'est decide dans Data Center.

## Close gate de ce child doc-only

Ce child est clos si les decisions d'architecture, policies et criteres d'acceptance sont poses. L'implementation est hors scope.
