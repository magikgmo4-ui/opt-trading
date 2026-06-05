---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01/20_HOT_PATH_AND_COLD_PATH_DESIGN.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01/30_COMPILED_INDEXES_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01/40_SOURCE_SELECTION_POLICY.md
---

# 90_REPRISE_POINT

## 7_CANONICAL_STATE

Child optimisation ouvert :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
```

## Architecture validee

```text
pro_desk_data_inventory.json + source_candidates.json (cold, source of truth)
        ↓
INDEX BUILDER (cold path, TARGET ~30ms rebuild)
        ↓
COMPILED INDEXES (5 index files in data/data_center/_registry/compiled/)
        ↓
MEMORY CACHE (hot path, TARGET ~405 KB, dict Python)
        ↓
SOURCE SELECTOR (hot path, TARGET <0.1ms per resolve)
        ↓
DATA CENTER VIEWS (canonical_value for consumers)
        ↓
DeskPro / Strategy / Perf / Telegram / Sheets / Dashboards
```

## Key decisions

```text
FORMAT       : JSON indexe en memoire (Python dict) — pas de dependance externe
MODULE       : modules/data_center/registry_cache.py + source_selector.py (spec only, not implemented)
REBUILD      : async, atomic swap, trigger par mtime/hash (design only)
MEMORY       : TARGET ~405 KB total (B04 pending)
LATENCY      : TARGET <0.1ms hot path, <50ms cold start (B01-B06 pending)
```

## Terminologie verrouillee

```text
Data Center arbitre les sources.
Data Center ne decide pas les trades.

Source Selector  → choisit la meilleure source candidate
Consumer         → utilise la donnee exposee
Strategy         → genere des signaux
Execution        → envoie les ordres
```

## Livrables

| # | Fichier | Statut |
|---|---|---|
| 00 | INITIAL_PROJECT_DOC | ✓ |
| 10 | RUNTIME_ACCESS_PROBLEM | ✓ |
| 20 | HOT_PATH_AND_COLD_PATH_DESIGN | ✓ |
| 30 | COMPILED_INDEXES_PLAN | ✓ |
| 40 | SOURCE_SELECTION_POLICY | ✓ |
| 50 | PERFORMANCE_BENCHMARK_PLAN | ✓ |
| 60 | LANGUAGE_AND_STORAGE_DECISION | ✓ |
| 90 | REPRISE_POINT | ✓ |

## 16_TODO

Prochaine etape : implementer `registry_cache.py` et `source_selector.py` selon ces specs, puis benchmarks B01-B08.
