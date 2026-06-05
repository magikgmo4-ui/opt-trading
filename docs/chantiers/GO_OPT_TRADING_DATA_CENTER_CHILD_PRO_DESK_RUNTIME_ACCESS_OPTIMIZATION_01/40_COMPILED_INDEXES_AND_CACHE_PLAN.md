---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01_COMPILED_INDEXES_PLAN
doc_type: design
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
---

# 30_COMPILED_INDEXES_PLAN

## Objet

Specifier les index compiles derives de `pro_desk_data_inventory.json` et `source_candidates.json`, generes par le cold path et consommes par le hot path.

## 1. Structure des index

```text
data/data_center/_registry/compiled/
├── by_contract_class.json       ← contract_class → [data_keys, producers, candidates]
├── by_data_key.json             ← data_key → [contract_class, producers, P-class, criticality]
├── by_source.json               ← producer_id → [data_keys, contracts covered]
├── by_priority.json             ← P0..P21 → [data_keys, criticality]
├── by_symbol.json               ← symbol → [available data_keys, last_write per producer]
└── _compiled.json               ← metadata (version, hash, build_ts)
```

## 2. by_contract_class.json

```json
{
  "market_metrics.v1": {
    "data_keys": ["open_interest", "funding_rate", "volume_futures", "long_short_ratio", "liquidations_long", "liquidations_short"],
    "producers": ["derivatives_collector__bitget", "derivatives_collector__binance"],
    "priority_class": ["P10", "P14"],
    "criticality": 6,
    "schema_ref": "schemas/market_metrics.v1.schema.json"
  },
  "pair_market_snapshot.v1": {
    "data_keys": ["last_price", "open", "high", "low", "close", "volume_24h"],
    "producers": ["collector_binance_spot"],
    "priority_class": ["P1"],
    "criticality": 3,
    "schema_ref": "schemas/pair_market_snapshot.v1.schema.json"
  }
}
```

## 3. by_data_key.json

```json
{
  "open_interest": {
    "contract_class": "market_metrics.v1",
    "producers": ["derivatives_collector__bitget", "derivatives_collector__binance", "bot_vision_headless__coinglass"],
    "sources": ["bitget_api", "binance_api", "coinglass_api"],
    "P_class": ["P10", "P14"],
    "criticality": 6,
    "unit": "USD",
    "description": "Interet ouvert futures"
  },
  "funding_rate": {
    "contract_class": "market_metrics.v1",
    "producers": ["derivatives_collector__bitget", "derivatives_collector__binance", "bot_vision_headless__coinglass"],
    "sources": ["bitget_api", "binance_api", "coinglass_api"],
    "P_class": ["P10", "P14"],
    "criticality": 6,
    "unit": "",
    "description": "Taux de financement perps"
  }
}
```

## 4. by_source.json

```json
{
  "derivatives_collector__bitget": {
    "contract_class": "market_metrics.v1",
    "data_keys": ["open_interest", "funding_rate", "volume_futures", "long_short_ratio", "liquidations_long", "liquidations_short"],
    "family": "derivatives",
    "output_path": "data/data_center/derivatives/derivatives_collector__bitget/",
    "score_components": {
      "source_reliability": 0.5,
      "freshness": 0.0,
      "completeness": 0.0
    },
    "last_write": null
  }
}
```

## 5. by_priority.json

```json
{
  "P1": {
    "label": "Prix tradables temps reel",
    "criticality": 3,
    "data_keys": ["last_price", "bid", "ask", "spread", "ohlcv_intraday", "ohlcv_daily"],
    "covered": ["last_price", "open", "high", "low", "close"],
    "missing": ["bid", "ask", "spread", "tick_data", "level_2", "level_3", "auction_price"],
    "coverage_pct": 20
  }
}
```

## 6. by_symbol.json

```json
{
  "BTCUSDT": {
    "available_data_keys": {
      "open_interest": {
        "producers": {
          "derivatives_collector__bitget": {"last_write": null, "value": null},
          "derivatives_collector__binance": {"last_write": null, "value": null}
        },
        "best_value": null,
        "stale": true
      },
      "last_price": {
        "producers": {
          "collector_binance_spot": {"last_write": null, "value": null}
        },
        "best_value": null,
        "stale": true
      }
    }
  }
}
```

## 7. Build pipeline

```text
1. WATCHDOG detecte changement (mtime ou hash)
2. INDEX BUILDER:
   a. parse pro_desk_data_inventory.json
   b. parse source_candidates.json
   c. parse producers.json
   d. cross-join data_keys ↔ producers ↔ sources
   e. build 5 index dicts
   f. write to data/data_center/_registry/compiled/
   g. update _compiled.json (version++, hash, build_ts)
3. MEMORY CACHE:
   a. load new compiled indexes
   b. atomic pointer swap
   c. old cache eligible for GC
```

## 8. Atomicite

```text
Le swap de cache est atomique :
  - Nouveau cache construit dans un dict separe
  - Pointeur `_active_cache` mis a jour en une operation
  - Aucune requete hot path ne voit un etat intermediaire
  - Si le build echoue, l'ancien cache reste actif
```
