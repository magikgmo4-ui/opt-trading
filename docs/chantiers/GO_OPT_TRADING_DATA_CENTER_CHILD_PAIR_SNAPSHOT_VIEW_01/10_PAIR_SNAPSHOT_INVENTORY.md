---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PAIR_SNAPSHOT_VIEW_01_PAIR_SNAPSHOT_INVENTORY
doc_type: inventory
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PAIR_SNAPSHOT_VIEW_01
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_PAIR_SNAPSHOT_INVENTORY

## Producers `pair_market_snapshot.v1`

| Producer | output_path_root | Coverage | Status |
|---|---|---|---|
| `collector_binance_spot` | `data/data_center/spot/collector_binance_spot/` | full | déclaré, `last_write: null` |

**Note** : le collector écrit dans son propre répertoire `modules/collector_binance_spot/outputs/` (via `config.paths.latest_path`). Le `output_path_root` dans `producers.json` est la cible DC canonique déclarée mais le write effectif vers `data/data_center/` n'est pas encore câblé au niveau collector (gap GAP-P03 hors périmètre de ce GO).

## Consumers `pair_market_snapshot.v1`

| Consumer | access_pattern | read_path (avant GO) | read_path (après GO) | Status |
|---|---|---|---|---|
| `desk_pro__spot_snapshot` | `latest_only` | `data/data_center/spot/collector_binance_spot/latest.json` ❌ | `data/data_center/views/pair_market_snapshot/latest.json` ✓ | not_started |

**Reader réel** : AUCUN — aucun fichier Python ne lit `desk_pro__spot_snapshot` ni le spot snapshot.

```bash
grep -rn "desk_pro__spot_snapshot\|pair_market_snapshot\|spot_snapshot" modules/ --include="*.py" -l
# → modules/collector_binance_spot/src/collector_binance_spot/normalize.py (produit le format)
# → modules/collector_binance_spot/src/collector_binance_spot/run.py (produit le format)
# → modules/data_center/pair_snapshot_view_writer.py (writer, ce GO)
# → modules/data_center/tests/test_pair_snapshot_view_writer.py (tests, ce GO)
# → modules/data_center/tests/test_contract_tests.py (contract tests, ce GO)
```

**Statut** : `not_started` correct. Aucun reader fantôme créé.

## Payload `pair_market_snapshot.v1` — structure

Produit par `normalize_pair_market_snapshot()` :

```json
{
  "contract_version": "v1",
  "schema_version": "v1",
  "module_id": "collector_binance_spot",
  "provider_id": "binance_spot",
  "run_id": "<run_id>",
  "generated_at": "<iso_ts>",
  "entity_type": "pair_market_snapshot",
  "records": [
    {
      "pair_symbol": "BTCUSDT",
      "base_asset": "BTC",
      "quote_asset": "USDT",
      "trading_status": "TRADING",
      "is_spot_trading_allowed": true,
      "last_price": "51200.00",
      "open_price_24h": "...",
      "high_price_24h": "...",
      "low_price_24h": "...",
      "price_change_percent_24h": "...",
      "volume_base_24h": "...",
      "volume_quote_24h": "...",
      "trade_count_24h": 111111,
      "window_open_at": "...",
      "window_close_at": "...",
      "weighted_avg_price_24h": "...",
      "source": {"provider_symbol": "BTCUSDT"}
    }
  ]
}
```

Différence clé avec `market_metrics.v1` : payload batch (`records: [...]`), pas per-symbol.

## Vue neutre `pair_market_snapshot` — état writer (au 2026-05-23)

`write_pair_market_snapshot_view()` (dans `modules/data_center/pair_snapshot_view_writer.py`) écrit :

```text
data/data_center/views/pair_market_snapshot/latest.json          ← payload complet
data/data_center/views/pair_market_snapshot/by_symbol/<SYM>.json ← 1 doc par record
```

`by_symbol/<SYM>.json` = métadonnées du batch + champs du record individuel (document self-contained).

## Récapitulatif

| Consumer | read_path correct | Reader réel | À migrer | Statut |
|---|---|---|---|---|
| `desk_pro__spot_snapshot` | Oui (après ce GO) | Non | — rien à migrer | not_started |
