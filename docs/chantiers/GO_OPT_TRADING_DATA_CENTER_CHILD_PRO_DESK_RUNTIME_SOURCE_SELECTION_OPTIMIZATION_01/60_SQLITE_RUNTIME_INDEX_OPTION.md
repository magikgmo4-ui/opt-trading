---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01_SQLITE_RUNTIME_INDEX_OPTION
doc_type: architecture_option
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 60_SQLITE_RUNTIME_INDEX_OPTION

## Objet

Evaluer SQLite WAL comme index runtime local pour les registries pro desk.

## Pourquoi SQLite V1

SQLite est adapte si le besoin est :

- local-first ;
- transactionnel ;
- simple a deployer ;
- sans service externe ;
- compatible Debian/headless ;
- rapide pour lookup indexe ;
- inspectable via CLI.

## Fichier cible possible

```text
data/data_center/runtime/pro_desk_runtime_index.sqlite
```

## Tables candidates

```text
data_inventory
source_candidates
source_scores
canonical_values
resolver_decisions
consumer_views
lineage_events
```

## Mode recommande

```text
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA temp_store=MEMORY;
```

## Index minimaux

```text
idx_inventory_data_key
idx_inventory_contract_class
idx_candidates_data_key
idx_candidates_producer_id
idx_candidates_contract_class
idx_scores_data_key_source_id
idx_resolver_decisions_data_key_timestamp
```

## Regle de prudence

SQLite n'est pas a imposer avant benchmark. Le child implementation devra comparer :

```text
compiled JSON indexes only
vs
SQLite runtime index
```

## Non-objectifs

- Pas de Postgres V1.
- Pas de Redis V1.
- Pas de service externe V1.
- Pas de migration runtime dans ce child doc-only.
