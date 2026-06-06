---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01_LANGUAGE_AND_STORAGE_DECISION
doc_type: decision
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
---

# 60_LANGUAGE_AND_STORAGE_DECISION

## Objet

Decider du format de stockage runtime pour les index compiles et le cache memoire, en alignement avec le stack existant (Python, JSON, SQLite).

## 1. Formats evalues

| Format | Read speed | Write speed | Memory | Schema | Tooling existant |
|---|---|---|---|---|---|
| JSON brut | ✗ (parse 150 KB) | ✓ | ✗ | ✗ | ✓ (deja en place) |
| JSON indexe | ✓ (dict lookup) | ✓ | ✓ | ✓ | ✓ (Python natif) |
| SQLite in-memory | ✓ (indexed query) | ✓ | ✓ | ✓ | ✓ (perf.db, market_metrics_writer) |
| Pickle | ✓ (deserialize) | ✓ | ✓ | ✗ | ✓ (Python natif) |
| msgpack | ✓✓ | ✓ | ✓✓ | ✗ | ✗ (nouvelle dep) |
| Parquet | ✓ (colonne) | ✗ | ✓✓ | ✓ | ✗ |

## 2. Decision

```text
CHOIX: JSON indexe en memoire (Python dict)

RATIONNEL:
  1. Zero dependance externe (pas de msgpack, pas de Parquet)
  2. Dict lookup O(1) natif en Python
  3. Les index compiles sont ecrits en JSON sur disque (debuggable, lisible)
  4. Au chargement, json.load() → dict Python → memoire
  5. Meme format que les registres existants (producers.json, consumers.json)
  6. SQLite serait overkill pour ~400 KB de donnees
  7. Pas de cout de serialisation/deserialisation supplementaire

CONTRE les autres:
  - SQLite: trop lourd pour 400 KB, queries inutiles
  - Pickle: non debuggable, risque securite
  - msgpack/Parquet: nouvelle dependance non justifiee
```

## 3. Format sur disque

```text
data/data_center/_registry/compiled/
├── by_contract_class.json       ← JSON identique au dict memoire
├── by_data_key.json
├── by_source.json
├── by_priority.json
├── by_symbol.json
└── _compiled.json               ← metadata

Format: JSON (utf-8, indent=2 pour debug, compact en production)
Taille estimee: ~150 KB total
```

## 4. Format en memoire

```python
# Structure du cache actif (module-level singleton)
_active_cache: dict = {
    "version": 1,
    "build_ts": "2026-06-05T12:00:00Z",
    "source_hash": "sha256...",
    "by_contract_class": {
        "market_metrics.v1": {
            "data_keys": ["open_interest", ...],
            "producers": ["derivatives_collector__bitget", ...],
            "priority_class": ["P10", "P14"],
            "criticality": 6
        }
    },
    "by_data_key": {
        "open_interest": {
            "contract_class": "market_metrics.v1",
            "producers": ["derivatives_collector__bitget", ...],
            "P_class": ["P10", "P14"],
            "criticality": 6,
            "unit": "USD"
        }
    },
    "by_source": { ... },
    "by_priority": { ... },
    "by_symbol": { ... }
}
```

## 5. Module Python

```text
modules/data_center/registry_cache.py

Fonctions:
  load_cache() → dict              # charge les index compiles en memoire
  rebuild_cache() → dict           # reconstruit depuis les sources JSON
  get_cache() → dict               # retourne le cache actif (hot path)
  invalidate_cache() → None        # force rebuild au prochain acces

Singleton:
  _cache: dict | None = None       # None = pas encore charge
  _cache_lock: threading.Lock      # protege le swap atomique
```

## 6. SQLite runtime index option

### 6.1 Pourquoi considerer SQLite

```text
Le repo utilise deja SQLite WAL (perf/perf.db, market_metrics_writer).
SQLite offre :
  - CREATE INDEX pour des lookup O(log n)
  - Transactions ACID (atomicite des rebuilds)
  - Zero-config, pas de serveur separe
  - :memory: mode pour cache en RAM
  - Requetes parametrables pour filtrage complexe
```

### 6.2 SQLite vs Python dict — comparaison

| Critere | Python dict (V1 default) | SQLite :memory: |
|---|---|---|
| Lookup speed | O(1) natif, ~50ns | O(log n) via index, ~1-5us |
| Memory (400 KB data) | ~405 KB | ~800 KB (overhead B-tree) |
| Rebuild speed | ~30ms (json.load + loop) | ~50ms (INSERT + CREATE INDEX) |
| Atomicite | Manuel (swap pointer) | Natif (transaction) |
| Query complexe | Code manuel | SQL declaratif |
| Debuggabilite | print(dict) | sqlite3 CLI |
| Dependance | Zero | Integre Python stdlib |
| Historique / lineage | Non (in-memory only) | Persistance disque possible |

### 6.3 Quand basculer vers SQLite

```text
V1 : Python dict (zero overhead, suffisant pour 400 KB)
V2 (conditionnel) : SQLite :memory: SI :
  - B01-B08 confirment dict < 0.1ms ✓ (rester sur dict)
  - OU besoin de requetes complexes (ex: "tous les data_keys P10 avec criticite >= 6")
  - OU besoin de persistance historique des decisions resolver
  - OU > 100 producers / > 1000 data_keys (echelle future)
```

### 6.4 SQLite pour le cold path (stockage froid)

```text
Usage recommande independamment du hot path :
  - Stocker l'historique des resolver_decision.v1
  - Stocker l'historique des source_score.v1
  - Table data_lineage : producer_id, data_key, ts, value, canonical
  - Requetes d'audit : "quand a-t-on change de source pour BTCUSDT open_interest ?"

Module cible : modules/data_center/resolver_history.py
Base : data/data_center/resolver_history.db (SQLite WAL)
```

### 6.5 Decision finale

```text
HOT PATH  → Python dict (V1, pas de SQLite pour < 400 KB)
COLD PATH → SQLite WAL pour lineage/audit/historique (optionnel, future)
SQLITE    → benchmarker avant de decider, pas rejete sans mesure
```

## 7. Integration avec le source selector

```python
# modules/data_center/source_selector.py

from modules.data_center.registry_cache import get_cache

def resolve(contract_class, symbol, data_key):
    cache = get_cache()  # O(1), jamais None en production
    
    # O(1) lookups
    contract_info = cache["by_contract_class"].get(contract_class)
    data_key_info = cache["by_data_key"].get(data_key)
    
    if not contract_info or not data_key_info:
        return stale_fallback()
    
    candidates = data_key_info["producers"]
    return select_best(candidates, symbol, data_key)
```
