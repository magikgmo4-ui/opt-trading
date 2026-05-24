---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE_POINT

## État au merge

- Branche : `go/GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01`
- Tests : **135 PASS** (125 existants + 10 nouveaux)
- Verdict : ACCEPTED

## Fichiers modifiés

```text
modules/data_center/registry/consumers.json              ← perf_engine read_path corrigé
modules/data_center/layout.py                            ← views/market_metrics/history/ ajouté
modules/data_center/tests/test_contract_tests.py         ← 6 tests full_history
modules/data_center/tests/test_layout.py                 ← 1 test history dir
modules/derivatives_collector/app/market_metrics_writer.py  ← write_market_metrics_history_view()
modules/derivatives_collector/tests/test_market_metrics_writer.py  ← TestWriteHistoryView (6 tests)
docs/chantiers/...                                       ← 4 fichiers docs
```

## État figé — consumers `full_history` `market_metrics.v1`

```text
perf_engine__replay_context → not_started, read_path=views/market_metrics/history/, aucun reader réel
```

## Règle atteinte

**Aucun consumer `market_metrics.v1` ne lit un `producer_id` path.** Tous les `access_pattern` couverts :
- `latest_only` → `views/market_metrics/latest.json`
- `by_symbol` → `views/market_metrics/by_symbol/<SYMBOL>.json`
- `full_history` → `views/market_metrics/history/`

## Etat global consumer coverage après ce GO

| access_pattern | Consumer | Status |
|---|---|---|
| `latest_only` | `desk_pro__market_metrics` | MIGRÉ (reader réel) |
| `latest_only` | `telegram_screener__signal_context` | not_started |
| `latest_only` | `google_sheets__market_reporting` | not_started |
| `by_symbol` | `strategy_framework__market_context` | not_started |
| `full_history` | `perf_engine__replay_context` | not_started (path corrigé ✓) |
| `status_only` | `localcms__data_center_health` | not_started |

## Prochaine étape

La règle "aucun consumer ne lit un producer_id" est **atteinte**. Le chantier PF_DATA_CENTER sur ce périmètre est complet.

Prochains GOs possibles selon priorité produit :
- Implémenter un consumer `not_started` réel (telegram, google_sheets, strategy_framework, perf_engine).
- Ajouter un producer (nouveau exchange).
- Enrichir le contrat `market_metrics.v1` (champ supplémentaire).
