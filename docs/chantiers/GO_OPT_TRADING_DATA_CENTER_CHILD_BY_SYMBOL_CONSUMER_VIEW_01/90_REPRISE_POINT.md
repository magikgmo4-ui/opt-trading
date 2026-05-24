---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE_POINT

## État au merge

- Branche : `go/GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01`
- Tests : **125 PASS** (121 existants + 4 nouveaux)
- Verdict : ACCEPTED

## Fichiers modifiés

```text
modules/data_center/tests/test_contract_tests.py        ← 4 tests by_symbol
modules/derivatives_collector/tests/test_market_metrics_writer.py  ← 1 test by_symbol découplagé
docs/chantiers/...                                       ← 5 fichiers docs
```

## État figé — consumers `by_symbol` `market_metrics.v1`

```text
strategy_framework__market_context → not_started (pas de reader, ne pas en créer)
```

## Etat global consumer coverage après ce GO

| access_pattern | Consumer | Status |
|---|---|---|
| `latest_only` | `desk_pro__market_metrics` | MIGRÉ (reader réel) |
| `latest_only` | `telegram_screener__signal_context` | not_started |
| `latest_only` | `google_sheets__market_reporting` | not_started |
| `by_symbol` | `strategy_framework__market_context` | not_started |
| `full_history` | `perf_engine__replay_context` | not_started |
| `status_only` | `localcms__data_center_health` | not_started |

## Prochaine étape

**Seul consumer non couvert par une vue neutre** : `perf_engine__replay_context` (`full_history`, `normalized/`).

Ce consumer lit encore directement le path producteur :
```text
data/data_center/derivatives/derivatives_collector__bitget/normalized/
```

Pour finaliser la règle "aucun consumer ne lit un producer_id", il faudra créer une vue historique :
```text
data/data_center/views/market_metrics/history/<SYMBOL>/
```
ou équivalent — GO dédié.
