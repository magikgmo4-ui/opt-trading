---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01_ACCEPTANCE_REPORT
doc_type: acceptance_report
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

## Résultats

| Suite | Résultat |
|---|---|
| `modules/data_center/tests/test_contract_tests.py` | **30/30 PASS** (+2 nouveaux) |
| `tests/test_desk_pro_market_metrics_reader.py` | **28/28 PASS** |
| `modules/derivatives_collector/tests/test_market_metrics_writer.py` | **42/42 PASS** |
| `modules/data_center/tests/test_layout.py` | **11/11 PASS** |
| `bash modules/data_center/scripts/sanity_check.sh` | **PASS** |
| `git diff --check` | **CLEAN** |
| **Total** | **121/121 PASS** |

## Critères de passage

| Critère | Statut |
|---|---|
| Tous les consumers `latest_only` ont `read_path` → `views/market_metrics/latest.json` | PASS |
| Aucun `read_path` `latest_only` ne contient `bitget`/`binance`/`derivatives_collector__` | PASS |
| `desk_pro` reste migré (`migration_needed: false`) | PASS |
| `telegram_screener` reste `not_started` | PASS |
| `google_sheets` reste `not_started` | PASS |
| Aucun reader fantôme créé | PASS |
| Aucun side effect Telegram/Sheets/DB | PASS |

## Verdict

**ACCEPTED**
