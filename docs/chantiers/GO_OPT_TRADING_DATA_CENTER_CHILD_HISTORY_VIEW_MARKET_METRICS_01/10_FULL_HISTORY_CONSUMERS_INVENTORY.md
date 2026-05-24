---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01_FULL_HISTORY_CONSUMERS_INVENTORY
doc_type: inventory
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_FULL_HISTORY_CONSUMERS_INVENTORY

## Périmètre

Consumers `market_metrics.v1` avec `access_pattern: full_history` dans `modules/data_center/registry/consumers.json`.

## Inventaire (au 2026-05-23)

### `perf_engine__replay_context`

**Avant ce GO :**
```json
{
  "consumer_id": "perf_engine__replay_context",
  "read_path": "data/data_center/derivatives/derivatives_collector__bitget/normalized/",
  "access_pattern": "full_history",
  "implementation_status": "not_started"
}
```

**Après ce GO :**
```json
{
  "consumer_id": "perf_engine__replay_context",
  "read_path": "data/data_center/views/market_metrics/history/",
  "access_pattern": "full_history",
  "implementation_status": "not_started"
}
```

**Reader réel** : AUCUN — aucun fichier Python dans `modules/` ne lit `normalized/` ni le path corrigé.

**Recherche effectuée** :
```bash
grep -r "derivatives_collector__bitget\|normalized/" modules/ --include="*.py" -l
# → modules/vision/coinglass/tests/test_telegram_summary.py  (contexte différent)
# → modules/vision/coinglass/tests/test_vision_context_v1.py (contexte différent)
# → modules/derivatives_collector/tests/test_market_metrics_writer.py (writer tests)
# → modules/derivatives_collector/app/market_metrics_writer.py (writer)
# → modules/data_center/tests/test_layout.py (layout)
# → modules/data_center/tests/test_contract_tests.py (contract tests)
```

Aucun de ces fichiers n'est un reader perf_engine. `modules/perf_engine/app/perf_engine.py` lit
depuis `data/perf` (positions + execution JSON), pas depuis `data/data_center/`.

**Statut** : `not_started` est correct. Ne pas créer de reader fantôme.

---

## Vue neutre `history` — état writer (au 2026-05-23)

`write_market_metrics_history_view()` écrit :

```text
data/data_center/views/market_metrics/history/<SYMBOL>/<run_id>.json
```

- `run_id` : paramètre optionnel, défaut = `metrics_ts` sanitisé (colons strippés).
- Accumulation : chaque appel crée un nouveau fichier, pas d'overwrite.
- Alimenté par : tout provider connu (bitget, binance_derivatives).

---

## Récapitulatif

| Consumer | read_path corrigé | Reader réel | À migrer | Statut |
|---|---|---|---|---|
| `perf_engine__replay_context` | Oui | Non | — rien à migrer | not_started |

## État global consumer coverage après ce GO

| access_pattern | Consumer | Status |
|---|---|---|
| `latest_only` | `desk_pro__market_metrics` | MIGRÉ (reader réel) |
| `latest_only` | `telegram_screener__signal_context` | not_started |
| `latest_only` | `google_sheets__market_reporting` | not_started |
| `by_symbol` | `strategy_framework__market_context` | not_started |
| `full_history` | `perf_engine__replay_context` | not_started (path corrigé ✓) |
| `status_only` | `localcms__data_center_health` | not_started |

**Règle** : aucun consumer ne lit un `producer_id` path. Règle atteinte.
