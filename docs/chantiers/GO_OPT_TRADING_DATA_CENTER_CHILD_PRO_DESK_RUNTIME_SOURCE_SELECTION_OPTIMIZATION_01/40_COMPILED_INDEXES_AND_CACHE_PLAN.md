---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01_COMPILED_INDEXES_AND_CACHE_PLAN
doc_type: architecture
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 40_COMPILED_INDEXES_AND_CACHE_PLAN

## Objectif

Eviter les scans complets de `pro_desk_data_inventory.json` et `source_candidates.json` dans le hot path.

## Indexes compiles cibles

```text
data/data_center/_compiled/pro_desk_inventory/by_data_key.json
data/data_center/_compiled/pro_desk_inventory/by_contract.json
data/data_center/_compiled/pro_desk_inventory/by_consumer.json
data/data_center/_compiled/pro_desk_inventory/by_priority.json
data/data_center/_compiled/source_candidates/by_data_key.json
data/data_center/_compiled/source_candidates/by_contract.json
data/data_center/_compiled/source_candidates/by_producer.json
data/data_center/_compiled/source_candidates/by_consumer_policy.json
```

## Snapshot memoire cible

```python
DataCenterRegistrySnapshot(
    inventory_version="v1",
    source_candidates_version="v1",
    inventory_checksum="...",
    candidates_checksum="...",
    loaded_at="...",
    indexes={
        "by_data_key": {},
        "by_contract": {},
        "by_producer": {},
        "by_consumer": {},
        "by_priority": {},
    },
)
```

## Regle de generation

Les indexes compiles sont derivés. Ils peuvent etre supprimes et reconstruits depuis les registries canoniques.

## Regle de lecture

Le resolver lit d'abord le snapshot. Il ne lit les JSON canoniques que si le snapshot manque ou est invalide.

## Regle d'ecriture

Toute ecriture de compiled index doit suivre :

```text
write temp
fsync
rename
```

## Criteres V1

- lookup par `data_key` sans scan complet ;
- lookup par `contract_class` sans scan complet ;
- lookup source candidates par producer ;
- trace checksum pour savoir quelle version a servi une selection ;
- fallback clair si compiled index absent.
