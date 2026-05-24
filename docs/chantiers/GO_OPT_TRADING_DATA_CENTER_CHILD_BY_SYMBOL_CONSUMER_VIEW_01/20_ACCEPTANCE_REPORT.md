---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01_ACCEPTANCE_REPORT
doc_type: acceptance_report
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

## Résultats

| Suite | Résultat |
|---|---|
| `modules/data_center/tests/test_contract_tests.py` | **32/32 PASS** (+4 nouveaux) |
| `modules/derivatives_collector/tests/test_market_metrics_writer.py` | **53/53 PASS** (+1 nouveau) |
| `tests/test_desk_pro_market_metrics_reader.py` | **28/28 PASS** |
| `modules/data_center/tests/test_layout.py` | **11/11 PASS** |
| `bash modules/data_center/scripts/sanity_check.sh` | **PASS** |
| `git diff --check` | **CLEAN** |
| **Total** | **125/125 PASS** |

## Critères de passage

| Critère | Statut |
|---|---|
| Consumer `by_symbol` `market_metrics.v1` : `read_path` → `views/market_metrics/by_symbol/` | PASS |
| Aucun `by_symbol` read_path ne contient `bitget`/`binance`/`derivatives_collector__` | PASS |
| `strategy_framework__market_context` reste `not_started` | PASS |
| Writer `by_symbol` découplagé du producer_id | PASS |
| Path `by_symbol` atteignable via `write_market_metrics_view()` | PASS |
| Aucun reader fantôme créé | PASS |

## Verdict

**ACCEPTED**
