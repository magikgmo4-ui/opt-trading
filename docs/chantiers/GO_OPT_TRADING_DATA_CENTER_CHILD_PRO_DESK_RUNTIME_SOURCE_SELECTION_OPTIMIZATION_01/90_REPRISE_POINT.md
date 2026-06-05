---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 90_REPRISE_POINT

## 7_CANONICAL_STATE

Child ouvert :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
```

Branche :

```text
go/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
```

## 1_MASTER_TARGET

Preparer l'optimisation runtime de `pro_desk_data_inventory.json` et `source_candidates.json`, maintenant en production et situes au centre du flux producer -> Data Center -> consumer.

## 4_MASTER_PROJECT_PLAN

1. Recherche multi-source data center.
2. Analyse risques runtime.
3. Hot path / cold path.
4. Compiled indexes + cache snapshot.
5. Source selection policy profiles.
6. Option SQLite runtime index.
7. Benchmark + acceptance criteria.

## 11_KEY_DECISIONS

- JSON canonique reste source of truth.
- Hot path ne doit pas scanner les JSON complets.
- Compiled indexes et cache snapshot sont la solution V1 par defaut.
- SQLite WAL est une option a benchmarker, pas une obligation immediate.
- Data Center arbitre la source ; les consumers decident l'usage.
- Toutes les candidates doivent etre preservees.
- Toute selection doit avoir policy + trace.

## 12_INVARIANTS

- Aucun runtime modifie dans ce child.
- Aucun registry production modifie dans ce child.
- Aucun reader consumer cree.
- Aucun producer path lu directement par consumer.
- Pas de decision trading dans Data Center.

## 15_REMAINING_GAP

- Benchmarks non executes.
- Implementation compile/index/cache non ouverte.
- Comparaison compiled JSON vs SQLite non faite.
- Tests atomic write / snapshot reload non faits.

## 16_TODO

Prochain child possible :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_INDEX_IMPLEMENTATION_01
```

Seulement apres validation du plan et des criteres benchmark.

## 17_RESUME_POINT

Reprendre par implementation benchmark-first : lire les registries production, mesurer cold load et scan actuel, puis implementer compiled indexes/cache snapshot sans changer la semantique de source selection.
