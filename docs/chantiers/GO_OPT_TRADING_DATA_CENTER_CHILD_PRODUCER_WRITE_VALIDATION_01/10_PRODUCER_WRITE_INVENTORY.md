---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01_INVENTORY
doc_type: inventory
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01
created_at: 2026-05-25
updated_at: 2026-05-25
---

# 10_PRODUCER_WRITE_INVENTORY

## Producers actifs — capacité write Data Center

### derivatives_collector__bitget

| Champ | Valeur |
|---|---|
| `contract_class` | `market_metrics.v1` |
| `output_path_root` | `data/data_center/derivatives/derivatives_collector__bitget/` |
| `write_function` | `write_market_metrics_to_data_center()` via `market_metrics_writer.py` |
| `last_write` (runtime) | `null` — pas de run prod confirmé |
| `coverage_status` | `full` (6/6 métriques) |
| `Statut write fixture` | **PROUVÉ** — `TestRuntimeRegistryIntegration.test_bitget_last_write_is_not_null_after_write` |

Câblage complet : `derivatives_collector` → `write_market_metrics_to_data_center()` → `data/data_center/derivatives/derivatives_collector__bitget/` → `update_producer_last_write()` → `data/data_center/_registry/producers.json`.

---

### derivatives_collector__binance

| Champ | Valeur |
|---|---|
| `contract_class` | `market_metrics.v1` |
| `output_path_root` | `data/data_center/derivatives/derivatives_collector__binance/` |
| `write_function` | `write_market_metrics_to_data_center()` via `market_metrics_writer.py` |
| `last_write` (runtime) | `null` — pas de run prod confirmé |
| `coverage_status` | `full` (6/6 métriques) |
| `Statut write fixture` | **PROUVÉ** — `TestRuntimeRegistryIntegration.test_binance_last_write_is_not_null_after_write` |

---

### collector_binance_spot

| Champ | Valeur |
|---|---|
| `contract_class` | `pair_market_snapshot.v1` |
| `output_path_root` | `data/data_center/spot/collector_binance_spot/` |
| `write_function` | `write_pair_market_snapshot_view()` → vues uniquement (views/) |
| `last_write` (runtime) | `null` |
| `coverage_status` | `full` |
| `Statut write` | **GAP-P03** — collector écrit dans `modules/collector_binance_spot/outputs/`, pas encore dans `data/data_center/spot/collector_binance_spot/` |

`write_pair_market_snapshot_view()` écrit dans `data/data_center/views/pair_market_snapshot/` (vue neutre),
pas dans le path producer `data/data_center/spot/collector_binance_spot/`. Le câblage complet
producer → DC est hors périmètre de ce GO.

---

## Runtime registry — structure après ce GO

Chemin : `data/data_center/_registry/producers.json` (runtime, gitignored)

```json
{
  "runtime_registry_version": "v1",
  "updated_at": "<timestamp>",
  "producers": {
    "derivatives_collector__bitget": {
      "producer_id": "derivatives_collector__bitget",
      "contract_class": "market_metrics.v1",
      "last_write": "<iso_timestamp>",
      "last_output_path": "data/data_center/derivatives/derivatives_collector__bitget/latest.json",
      "status": "ok",
      "evidence": {"symbol": "BTCUSDT", "provider_id": "bitget"},
      "updated_at": "<iso_timestamp>"
    }
  }
}
```

---

## Séparation statique / runtime

| Registry | Chemin | Rôle | Mutable par write |
|---|---|---|---|
| Statique producers | `modules/data_center/registry/producers.json` | Contrats déclarés / schémas | **Non** |
| Statique consumers | `modules/data_center/registry/consumers.json` | Contrats consumers / read_path | **Non** |
| Runtime producers | `data/data_center/_registry/producers.json` | État vivant / last_write / evidence | **Oui** |

---

## Gaps restants après ce GO

| Gap | Producer | Description |
|---|---|---|
| GAP-P01 | `derivatives_collector__bitget` | `last_write: null` en prod — run réel non encore exécuté |
| GAP-P02 | `derivatives_collector__binance` | `last_write: null` en prod — idem |
| GAP-P03 | `collector_binance_spot` | Câblage `write_pair_market_snapshot_view()` vers producer path `data/data_center/spot/` non fait |
| GAP-P04 | `coinglass` | `NOT_PROVEN_RUNTIME_ADAPTER` permanent |
