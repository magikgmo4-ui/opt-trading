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
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01/30_HOT_PATH_COLD_PATH_ARCHITECTURE.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01/40_COMPILED_INDEXES_AND_CACHE_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01/50_SOURCE_SELECTION_POLICY_PROFILES.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01/70_BENCHMARK_AND_ACCEPTANCE_CRITERIA.md
---

# 90_REPRISE_POINT

## 7_CANONICAL_STATE

Child optimisation fusionne — structure 9 fichiers :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
```

Fusion des specs `RUNTIME_ACCESS_OPTIMIZATION` + `RUNTIME_SOURCE_SELECTION_OPTIMIZATION` en un seul child canonique.

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
FORMAT       : JSON indexe en memoire (Python dict) — zero dependance V1
              SQLite WAL = option cold path (audit/history), pas hot path
MODULE       : modules/data_center/registry_cache.py + source_selector.py (spec only)
REBUILD      : async, atomic swap, trigger par mtime/hash
MEMORY       : TARGET ~405 KB total (B04 pending)
LATENCY      : TARGET <0.1ms hot path, <50ms cold start (B01-B06 pending)
SELECTOR     : 4 modes (best_candidate, all_candidates, consensus, fallback_only)
BENCHMARKS   : B01-B08 + AC01-AC14 go criteria + NG01-NG08 no-go criteria
RISKS        : R01-R10 analyses + mitigations
```

## Terminologie verrouillee

```text
Data Center arbitre les sources.
Data Center ne decide pas les trades.

Source Selector → choisit la meilleure source candidate selon policy + scoring
Consumer        → utilise la donnee exposee, ne choisit pas les sources brutes
Strategy        → genere des signaux
Execution       → envoie les ordres
```

## Livrables (9 fichiers)

| # | Fichier | Contenu |
|---|---|---|
| 00 | INITIAL_PROJECT_DOC | Plan + scope fusionne |
| 10 | RESEARCH_FINDINGS | MDM, data contracts, Bloomberg/Refinitiv/Coinglass precedents |
| 20 | CURRENT_RUNTIME_RISK_ANALYSIS | Probleme technique + R01-R10 |
| 30 | HOT_PATH_COLD_PATH_ARCHITECTURE | Diagramme ASCII + regles hot/cold |
| 40 | COMPILED_INDEXES_AND_CACHE_PLAN | 5 indexes + schemas JSON + atomic swap |
| 50 | SOURCE_SELECTION_POLICY_PROFILES | 4 modes + policy profiles |
| 60 | LANGUAGE_STORAGE_AND_SQLITE_DECISION | Matrice 6 formats + SQLite option |
| 70 | BENCHMARK_AND_ACCEPTANCE_CRITERIA | B01-B08 + AC01-AC14 + NG01-NG08 |
| 90 | REPRISE_POINT | Resume + next GO |

## 16_TODO

```text
NEXT_GO = GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_INDEX_IMPLEMENTATION_01

Cible : benchmark-first → compiled indexes → cache snapshot → source selection fast path

Avant implementation :
  - Executer B01-B08 (baseline JSON parse + target dict lookup)
  - Valider AC01-AC14
  - Verifier NG01-NG08 non declenches
```
