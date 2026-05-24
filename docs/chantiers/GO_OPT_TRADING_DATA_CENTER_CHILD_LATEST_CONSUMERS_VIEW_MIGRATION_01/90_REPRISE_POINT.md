---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE_POINT

## État au merge

- Branche : `go/GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01`
- Tests : **121 PASS** (119 existants + 2 nouveaux invariants)
- Verdict : ACCEPTED

## Fichiers modifiés

```text
modules/data_center/tests/test_contract_tests.py   ← 2 nouveaux tests
docs/chantiers/...                                  ← 5 fichiers docs
```

## État figé des consumers `latest_only`

```text
desk_pro__market_metrics      → MIGRÉ  (reader réel, views/ primary, legacy fallback)
telegram_screener__signal_context → not_started (pas de reader, ne pas en créer)
google_sheets__market_reporting   → not_started (pas de reader, ne pas en créer)
```

## Prochaines étapes

### Court terme
- **Supprimer le fallback legacy** dans `market_metrics_reader.py` une fois que `data/data_center/views/market_metrics/` est alimenté de manière fiable par le pipeline de production.
- **Valider `sanity_check.sh`** : `consumers implemented: 1` est correct aujourd'hui.

### Moyen terme
- Implémenter `telegram_screener__signal_context` : son reader devra lire `DC_MARKET_METRICS_VIEW` en primary.
- Implémenter `google_sheets__market_reporting` : idem, avec `fallback: error` (raise si absent).

### Long terme
- `strategy_framework__market_context` (`by_symbol`) et `perf_engine__replay_context` (`full_history`) : nécessitent des vues dédiées dans `data/data_center/views/market_metrics/` — GOs séparés.
