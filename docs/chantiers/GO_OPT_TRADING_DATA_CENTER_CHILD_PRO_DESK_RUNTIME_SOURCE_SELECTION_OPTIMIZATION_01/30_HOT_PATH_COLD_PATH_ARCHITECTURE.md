---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01_HOT_PATH_COLD_PATH_ARCHITECTURE
doc_type: architecture
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 30_HOT_PATH_COLD_PATH_ARCHITECTURE

## Objet

Separer les operations lentes, completes et auditables des operations rapides demandees par les consumers.

## Cold path

Le cold path travaille sur les sources canoniques :

```text
modules/data_center/registry/pro_desk_data_inventory.json
modules/data_center/registry/source_candidates.json
```

Operations cold path :

- validation complete ;
- schema checks ;
- cross-reference producer/consumer ;
- detection orphan data_key/source_id ;
- generation compiled indexes ;
- generation runtime SQLite optionnel ;
- rapport health / sanity.

Le cold path peut etre plus lent. Il est execute par job, CI, sanity check ou reload manuel.

## Hot path

Le hot path repond aux consumers :

```text
get_best_candidate(data_key, symbol, consumer_policy)
get_all_candidates(data_key, symbol)
get_view(contract_class, symbol)
```

Operations hot path autorisees :

- lookup indexe ;
- lecture snapshot memoire ;
- selection candidate deja indexee ;
- verification freshness locale ;
- emission trace legere.

Operations hot path interdites :

- full JSON load ;
- scan complet P0-P21 ;
- validation complete de tous les producers ;
- recalcul global de tous les scores ;
- lecture directe des producer paths par consumer.

## Flux cible

```text
canonical JSON
-> compile step
-> compiled indexes / sqlite runtime index
-> registry snapshot
-> source selector
-> materialized Data Center views
-> consumers
```

## Invalidation

Reload snapshot uniquement si :

- checksum change ;
- mtime change ;
- version registry change ;
- commande reload explicite.
