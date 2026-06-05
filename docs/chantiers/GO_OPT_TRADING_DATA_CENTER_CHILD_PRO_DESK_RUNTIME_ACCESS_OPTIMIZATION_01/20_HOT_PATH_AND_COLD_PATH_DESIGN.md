---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01_HOT_COLD_PATH
doc_type: design
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
---

# 20_HOT_PATH_AND_COLD_PATH_DESIGN

## Objet

Separer les chemins d'acces chauds (lus a chaque requete consumer) et froids (lus a l'initialisation ou rarement), pour que le hot path n'ait jamais a parser un fichier JSON complet.

## 1. Architecture

```text
              ┌─────────────────────────────────────────┐
COLD PATH     │  pro_desk_data_inventory.json           │
(init /       │  source_candidates.json                 │
 rare)        │  producers.json / consumers.json        │
              └──────────────┬──────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   INDEX BUILDER  │  ← compile les index une fois
                    │   (cold, async)  │
                    └────────┬────────┘
                             │
              ┌──────────────▼──────────────────────────┐
              │           COMPILED INDEXES               │
              │  ┌──────────────────────────────────┐    │
              │  │ by_contract_class.json           │    │
              │  │ by_data_key.json                 │    │
              │  │ by_source.json                   │    │
              │  │ by_priority.json                 │    │
              │  │ by_symbol.json                   │    │
              │  └──────────────────────────────────┘    │
              └──────────────┬──────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  MEMORY CACHE   │  ← kept in RAM
                    │  (hot, sync)    │
                    └────────┬────────┘
                             │
              ┌──────────────▼──────────────────────────┐
HOT PATH      │         SOURCE SELECTOR                  │
(read every   │  ┌──────────────────────────────────┐    │
 request)     │  │ resolve(contract, symbol, key)    │    │
              │  │ validate_schema(payload)          │    │
              │  │ is_stale(ts, max_age)             │    │
              │  │ get_candidates(contract, key)     │    │
              │  └──────────────────────────────────┘    │
              └──────────────┬──────────────────────────┘
                             │
              ┌──────────────▼──────────────────────────┐
              │          DATA CENTER VIEWS               │
              │  canonical_value for consumers          │
              └─────────────────────────────────────────┘
```

## 2. Hot path — ce qui doit etre < 5ms

```text
resolve(contract_class, symbol, data_key):
  1. by_contract_class[contract_class]        → O(1) dict lookup
  2. by_data_key[data_key]                    → O(1) dict lookup
  3. get candidates for (contract, data_key)  → O(1) list lookup
  4. for each candidate: check freshness      → O(n) n≤5 max
  5. for each candidate: check eligibility    → O(n)
  6. select best score                        → O(n)
  7. return canonical_value                   → O(1)

Total: O(n) where n = nombre de sources candidates (≤5 actuellement)
```

Ce qui est EXCLU du hot path :
- Lecture de fichier JSON
- Parsing de ~150 KB
- Iteration sur 500 champs
- Appel API externe
- Ecriture disque

## 3. Cold path — ce qui peut prendre > 100ms

```text
INDEX REBUILD (triggered by inventory change):
  1. parse pro_desk_data_inventory.json       → ~5ms
  2. parse source_candidates.json             → ~2ms
  3. parse producers.json                     → ~1ms
  4. parse consumers.json                     → ~1ms
  5. build by_contract_class index            → ~3ms
  6. build by_data_key index                  → ~5ms
  7. build by_source index                    → ~2ms
  8. build by_priority index                  → ~2ms
  9. write compiled index files               → ~10ms
  10. refresh memory cache                    → ~1ms

Total rebuild: ~30ms — acceptable car declenche rarement
```

## 4. Cache invalidation

```text
TRIGGERS de rebuild :
  - Modification de pro_desk_data_inventory.json
  - Modification de source_candidates.json
  - Ajout/retrait producer dans producers.json
  - Changement de contract schema

STRATEGY :
  - Watchdog sur les fichiers registry (mtime)
  - Hash SHA256 des fichiers pour detection
  - Rebuild async, swap atomique du cache
  - Le hot path utilise toujours le cache actif (jamais bloque)
```

## 5. Memory budget

```text
pro_desk_data_inventory.json (parsed):    ~200 KB
source_candidates.json (parsed):          ~50 KB
by_contract_class index:                  ~30 KB
by_data_key index:                        ~80 KB
by_source index:                          ~20 KB
by_priority index:                        ~15 KB
by_symbol index:                          ~10 KB
----------------------------------------
TOTAL cache memoire:                     ~405 KB

Negligeable. Aucun besoin de cache distribue.
```
