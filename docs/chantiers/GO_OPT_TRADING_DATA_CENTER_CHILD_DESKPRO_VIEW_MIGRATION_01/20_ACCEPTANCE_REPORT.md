---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01_ACCEPTANCE_REPORT
doc_type: acceptance_report
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

## Résultats

| Suite | Résultat |
|---|---|
| `tests/test_desk_pro_market_metrics_reader.py` | **28/28 PASS** |
| `modules/data_center/tests/test_contract_tests.py` | **28/28 PASS** |
| `modules/derivatives_collector/tests/test_market_metrics_writer.py` | **42/42 PASS** |
| `modules/data_center/tests/test_layout.py` | **11/11 PASS** |
| `bash modules/data_center/scripts/sanity_check.sh` | **PASS** |
| `git diff --check` | **CLEAN** |
| **Total** | **119 PASS** |

## Critères de passage

| Critère | Statut |
|---|---|
| Desk Pro lit `data/data_center/views/market_metrics/latest.json` par défaut | PASS |
| Fallback `data/deskpro/inputs/market_metrics/latest.json` fonctionne | PASS |
| Fallback sur DC invalide → legacy valide | PASS |
| Les deux absents → `[]` | PASS |
| Aucun path par défaut ne contient `bitget`/`binance`/`producer_id` | PASS |
| Tests existants non cassés | PASS |

## Verdict

**ACCEPTED**
