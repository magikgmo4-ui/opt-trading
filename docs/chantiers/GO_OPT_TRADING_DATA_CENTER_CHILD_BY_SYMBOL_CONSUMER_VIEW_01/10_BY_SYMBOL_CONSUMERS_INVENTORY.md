---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01_BY_SYMBOL_CONSUMERS_INVENTORY
doc_type: inventory
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_BY_SYMBOL_CONSUMERS_INVENTORY

## Périmètre

Consumers `market_metrics.v1` avec `access_pattern: by_symbol` dans `modules/data_center/registry/consumers.json`.

## Inventaire (au 2026-05-23)

### `strategy_framework__market_context`

```json
{
  "consumer_id": "strategy_framework__market_context",
  "contract_class": "market_metrics.v1",
  "read_path": "data/data_center/views/market_metrics/by_symbol/",
  "access_pattern": "by_symbol",
  "fallback": "stale_ok",
  "implementation_status": "not_started",
  "migration_needed": false,
  "read_path_current": null
}
```

**Reader réel** : AUCUN — aucun fichier Python dans `modules/` ne lit cette donnée.

**Recherche effectuée** :
```bash
find modules/ -name "*.py" | xargs grep -l "strategy_framework\|market_context\|by_symbol"
# → modules/collector_binance_spot/src/collector_binance_spot/normalize.py
#   modules/data_center/layout.py
#   modules/data_center/tests/test_contract_tests.py
#   modules/data_center/tests/test_layout.py
#   modules/derivatives_collector/app/market_metrics_writer.py
#   modules/derivatives_collector/tests/test_market_metrics_writer.py
```

Aucun de ces fichiers n'est un reader Strategy Framework. `normalize.py` utilise `by_symbol` dans un contexte différent (Binance spot).

**Statut** : `not_started` est correct. Ne pas créer de reader fantôme.

**Prochaine étape** : quand `PF_STRATEGY_FRAMEWORK_REGISTRY` sera implémenté, son reader devra lire `data/data_center/views/market_metrics/by_symbol/<SYMBOL>.json`. Fallback déclaré : `stale_ok` (données stales tolérées pour la stratégie).

---

## Vue neutre `by_symbol` — état writer (au 2026-05-23)

`write_market_metrics_view()` écrit déjà :

```text
data/data_center/views/market_metrics/by_symbol/<SYMBOL>.json
```

Alimenté par : `bitget`, `binance_derivatives` (tout provider connu). Dernier write wins par symbole.

**Couverture tests writer** :
- `test_view_writes_by_symbol` : path BTCUSDT correct
- `test_view_by_symbol_decoupled_from_producer_id` (nouveau) : binance = bitget sur le path by_symbol, aucun producer_id dans le path

---

## Récapitulatif

| Consumer | read_path correct | Reader réel | À migrer | Statut |
|---|---|---|---|---|
| `strategy_framework__market_context` | Oui | Non | — rien à migrer | not_started |

## Autres consumers hors périmètre `by_symbol`

| Consumer | access_pattern | Note |
|---|---|---|
| `desk_pro__market_metrics` | `latest_only` | migré (#753) |
| `telegram_screener__signal_context` | `latest_only` | not_started (#755) |
| `google_sheets__market_reporting` | `latest_only` | not_started (#755) |
| `perf_engine__replay_context` | `full_history` | `normalized/` — vue historique, GO futur |
| `localcms__data_center_health` | `status_only` | lit `_registry/producers.json` — hors `market_metrics.v1` |
