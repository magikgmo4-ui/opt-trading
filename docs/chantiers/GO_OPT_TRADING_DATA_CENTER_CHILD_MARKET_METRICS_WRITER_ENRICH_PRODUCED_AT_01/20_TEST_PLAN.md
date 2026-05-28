---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01_TEST_PLAN
doc_type: test_plan
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01
created_at: 2026-05-28
---

# 20_TEST_PLAN

## Tests existants à préserver

| Suite | Comptage |
|-------|----------|
| `modules/derivatives_collector/tests/test_market_metrics_writer.py` | 65 PASS |
| `modules/data_center/tests/test_contract_tests.py` | 44 PASS |
| `modules/data_center/tests/test_runtime_registry.py` | 11 PASS |
| `tests/data_center/test_schema_validator.py` | mis à jour (payloads new format) |
| `tests/data_center/test_schemas.py` | inchangé |

## Nouveaux tests

Fichier : `tests/derivatives_collector/test_market_metrics_writer_dc_alignment.py`

8 nouveaux tests (enrich_produced_at + DC writer validation + manifest).

## Commande de vérification

```bash
python3 -m pytest modules/derivatives_collector/tests/test_market_metrics_writer.py -q  # 65 PASS
python3 -m pytest modules/data_center/tests/ -q  # 44 + 11 PASS
python3 -m pytest tests/data_center/ -q  # 35 + updates PASS
```
