---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01_PRODUCER_INVENTORY
doc_type: producer_inventory
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_PRODUCER_INVENTORY — Contrats producers Data Center

## Objet

Inventaire des producers connus avec leur contrat Data Center formalisé et le mapping depuis leur output existant vers les paths `data/data_center/`.

---

## P1 — `derivatives_collector__bitget`

```yaml
producer_id: derivatives_collector__bitget
family: derivatives
schema_version: v1
contract_class: market_metrics.v1
output_path_root: data/data_center/derivatives/derivatives_collector__bitget/
write_mode: atomic
latency_class: oneshot
run_trigger: manual
collectable_metrics:
  - open_interest
  - funding_rate
  - volume_futures
missing_metrics:
  - long_short_ratio       # dépend Coinglass — not_proven_runtime_adapter
  - liquidations_long      # dépend Coinglass — not_proven_runtime_adapter
  - liquidations_short     # dépend Coinglass — not_proven_runtime_adapter
coverage_status: partial
validated_at: 2026-05-23
notes: >
  Implémenté dans modules/derivatives_collector/app/market_metrics_writer.py.
  Écrit actuellement vers data/collectors/derivatives/ et data/deskpro/inputs/market_metrics/.
  Adapter vers data/data_center/ sans casser les paths existants (extension, pas remplacement).
```

### Mapping output existant → Data Center

| Output actuel | Path Data Center cible |
|---|---|
| `data/collectors/derivatives/latest.json` | `data/data_center/derivatives/derivatives_collector__bitget/latest.json` |
| `data/collectors/derivatives/cache/by_symbol/<SYMBOL>.json` | `data/data_center/derivatives/derivatives_collector__bitget/cache/by_symbol/<SYMBOL>.json` |
| `data/collectors/derivatives/raw/` | `data/data_center/derivatives/derivatives_collector__bitget/raw/` |
| `data/collectors/derivatives/normalized/` | `data/data_center/derivatives/derivatives_collector__bitget/normalized/` |
| `data/collectors/derivatives/events.jsonl` | `data/data_center/derivatives/derivatives_collector__bitget/events.jsonl` |
| `data/collectors/derivatives/errors.jsonl` | `data/data_center/derivatives/derivatives_collector__bitget/errors.jsonl` |

Note : les paths `data/deskpro/inputs/market_metrics/` restent valides comme surface consumer Desk Pro. Ils ne sont pas remplacés par le Data Center — ils sont consommés depuis le Data Center via un consumer contract dédié (couvert dans `GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01`).

---

## P2 — `derivatives_collector__binance`

```yaml
producer_id: derivatives_collector__binance
family: derivatives
schema_version: v1
contract_class: market_metrics.v1
output_path_root: data/data_center/derivatives/derivatives_collector__binance/
write_mode: atomic
latency_class: oneshot
run_trigger: manual
collectable_metrics:
  - open_interest
  - funding_rate
  - volume_futures
missing_metrics:
  - long_short_ratio
  - liquidations_long
  - liquidations_short
coverage_status: partial
validated_at: null
notes: >
  Adapter Binance présent dans modules/derivatives_collector/app/binance_adapter.py.
  Couverture metrics à valider par test smoke avant de mettre validated_at.
  Même contract_class que Bitget : market_metrics.v1.
```

---

## P3 — `collector_binance_spot`

```yaml
producer_id: collector_binance_spot
family: spot
schema_version: v1
contract_class: pair_market_snapshot.v1
output_path_root: data/data_center/spot/collector_binance_spot/
write_mode: atomic
latency_class: oneshot
run_trigger: manual
collectable_metrics:
  - last_price
  - open_price_24h
  - high_price_24h
  - low_price_24h
  - volume_24h
  - quote_volume_24h
  - price_change_24h
  - price_change_pct_24h
  - trading_status
missing_metrics: []
coverage_status: full
validated_at: null
notes: >
  Implémenté via collectors_core (modules/collector_binance_spot/).
  Le format normalisé existant devient pair_market_snapshot.v1 — nomination Data Center
  du format déjà produit par normalize_pair_market_snapshot().
  validated_at à renseigner après premier smoke test Data Center path.
```

### Champs `pair_market_snapshot.v1` (contract_class à formaliser)

```json
{
  "contract_version": "v1",
  "input_class": "pair_market_snapshot.v1",
  "module_id": "collector_binance_spot",
  "provider_id": "binance",
  "snapshot_ts": "<ISO Z>",
  "freshness_state": "fresh | stale | unknown",
  "records": [
    {
      "pair_symbol": "BTCUSDT",
      "base_asset": "BTC",
      "quote_asset": "USDT",
      "trading_status": "TRADING",
      "last_price": "67000.00",
      "open_price_24h": "65000.00",
      "high_price_24h": "68000.00",
      "low_price_24h": "64000.00",
      "volume_24h": "12345.00",
      "quote_volume_24h": "820000000.00",
      "price_change_24h": "2000.00",
      "price_change_pct_24h": "3.08"
    }
  ]
}
```

Note : `pair_market_snapshot.v1` est la nomination canonique Data Center du format produit par `normalize_pair_market_snapshot()`. Son implémentation Python est à déclarer dans un child GO dédié (hors scope de ce child doc-first).

### Mapping output existant → Data Center

| Output actuel (`collectors_core`) | Path Data Center cible |
|---|---|
| `data/collectors/spot/binance_spot/latest.json` | `data/data_center/spot/collector_binance_spot/latest.json` |
| `data/collectors/spot/binance_spot/raw/` | `data/data_center/spot/collector_binance_spot/raw/` |
| `data/collectors/spot/binance_spot/normalized/` | `data/data_center/spot/collector_binance_spot/normalized/` |
| `data/collectors/spot/binance_spot/events.jsonl` | `data/data_center/spot/collector_binance_spot/events.jsonl` |
| `data/collectors/spot/binance_spot/errors.jsonl` | `data/data_center/spot/collector_binance_spot/errors.jsonl` |

---

## Hors scope — producers à traiter dans un child ultérieur

| Producer | Raison du report |
|---|---|
| `collector_coingecko` | Couverture réelle à confirmer (présent dans modules/ mais non audité ici) |
| `vision_bot / bot_vision_step2` | Producteur d'artefacts vision — family à définir (`vision`) |
| `webhook_server` | Producteur d'events Webhook/TV — contrat à définir (`events`) |
| `telegram_ingestion` | Non opérationnel à ce stade |

---

## Registre `producers.json` — état à la livraison de ce child

```json
{
  "registry_version": "v1",
  "updated_at": "2026-05-23T00:00:00Z",
  "producers": [
    {
      "producer_id": "derivatives_collector__bitget",
      "family": "derivatives",
      "contract_class": "market_metrics.v1",
      "schema_version": "v1",
      "output_path_root": "data/data_center/derivatives/derivatives_collector__bitget/",
      "coverage_status": "partial",
      "validated_at": "2026-05-23",
      "last_write": null
    },
    {
      "producer_id": "derivatives_collector__binance",
      "family": "derivatives",
      "contract_class": "market_metrics.v1",
      "schema_version": "v1",
      "output_path_root": "data/data_center/derivatives/derivatives_collector__binance/",
      "coverage_status": "partial",
      "validated_at": null,
      "last_write": null
    },
    {
      "producer_id": "collector_binance_spot",
      "family": "spot",
      "contract_class": "pair_market_snapshot.v1",
      "schema_version": "v1",
      "output_path_root": "data/data_center/spot/collector_binance_spot/",
      "coverage_status": "full",
      "validated_at": null,
      "last_write": null
    }
  ]
}
```

Ce fichier JSON est la spec du contenu à créer dans `GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01`. Il n'est pas encore un fichier runtime.

---

## BUNDLE_TARGET atteint

Ce child GO est fermable :
- [x] `10_PRODUCER_CONTRACT_SPEC.md` livré
- [x] `20_PRODUCER_INVENTORY.md` livré avec contrats pour `derivatives_collector__bitget`, `derivatives_collector__binance`, `collector_binance_spot`
- [x] Mapping vers paths `data/data_center/` documenté
- [x] Registre `producers.json` spécifié

Prochain child : `GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01`.
