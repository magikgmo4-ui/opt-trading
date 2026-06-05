---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01_PERFORMANCE_BENCHMARK_PLAN
doc_type: plan
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
---

# 50_PERFORMANCE_BENCHMARK_PLAN

## Objet

Definir les benchmarks de performance pour valider l'optimisation d'acces runtime.

## 1. Baseline (sans optimisation)

```text
Test: resolve("market_metrics.v1", "BTCUSDT", "open_interest") × 1000 appels

SANS optimisation :
  - Parse pro_desk_data_inventory.json (150 KB)    → ~5ms par appel
  - Parse source_candidates.json (30 KB)           → ~2ms par appel
  - Parse producers.json (3 KB)                    → ~1ms par appel
  - Cross-join data                                  → ~3ms par appel
  - TOTAL par appel                                → ~11ms
  - 1000 appels                                    → ~11 secondes
  - Latence p50                                    → ~10ms
  - Latence p99                                    → ~25ms
```

## 2. Cible (avec optimisation)

```text
AVEC optimisation (index compiles + cache memoire) :
  - dict lookup by_contract_class                  → <0.001ms
  - dict lookup by_data_key                        → <0.001ms
  - list candidates                                → <0.001ms
  - freshness check (2 sources)                    → <0.01ms
  - eligibility check                              → <0.01ms
  - select best                                    → <0.01ms
  - TOTAL par appel (TARGET)                       → <0.1ms
  - 1000 appels (TARGET)                           → <0.1 seconde
  - Latence p50 (TARGET)                           → <0.05ms
  - Latence p99 (TARGET)                           → <0.5ms
```

## 3. Benchmarks a implementer

### B01 — resolve() single call

```text
Input:  resolve("market_metrics.v1", "BTCUSDT", "open_interest")
Metric: wall-clock time
Target: < 0.1ms (avec cache chaud)
        < 5ms (avec cold cache, premier appel apres rebuild)
```

### B02 — resolve() throughput

```text
Input:  10 000 resolve() calls, mixed contract_class/data_key/symbol
Metric: calls/second
Target: > 50 000 calls/second
```

### B03 — Cache rebuild time

```text
Input:  modification de pro_desk_data_inventory.json
Metric: time from change detection to hot cache active
Target: < 50ms
```

### B04 — Memory footprint

```text
Input:  cache chaud + tous les index compiles
Metric: RSS memory delta
Target: < 5 MB
```

### B05 — Concurrent access

```text
Input:  10 consumers concurrents, chacun 1000 resolve()
Metric: p99 latency, no deadlock
Target: p99 < 2ms, 0 deadlock
```

### B06 — Cold start

```text
Input:  process start, premier resolve()
Metric: time to first response
Target: < 50ms (incluant build index + cache)
```

### B07 — Stale fallback path

```text
Input:  resolve() where 0 candidates have fresh data
Metric: response time
Target: < 0.1ms (meme chemin que hot path, retourne stale)
```

### B08 — JSON parse vs index lookup comparison

```text
Input:  1000 iterations, JSON parse vs dict lookup for same data_key
Metric: speedup ratio
Target: > 100x faster with index
```

## 4. Regression tests

```text
- Apres chaque modification d'inventaire, re-run B01-B08
- Apres chaque ajout de producer, re-run B01-B08
- Apres chaque ajout de consumer, re-run B03 (cache rebuild)
- Seuil d'alerte: p99 > 2ms ou rebuild > 100ms
```
