---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01_TEST_PLAN
doc_type: test_plan
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01
status: open
created_at: 2026-05-28
updated_at: 2026-05-28
---

# 20_TEST_PLAN

## Tests existants à préserver

| Suite | Comptage |
|-------|----------|
| `tests/data_center/` | 24 PASS (inchangés) |
| `modules/collector_binance_spot/tests/test_binance_spot_module.py` | 7 tests PASS (inchangés) |
| `modules/data_center/tests/test_spot_snapshot_dc_writer.py` | 10 tests PASS (inchangés) |

## Nouveaux tests

Fichier : `tests/data_center/test_binance_spot_dc_runtime.py`

| # | Test | Vérification |
|---|------|-------------|
| 1 | `test_pair_market_snapshot_v1_registered` | Schema dans le registry |
| 2 | `test_validate_valid_pair_market_snapshot` | Payload normalisé valide |
| 3 | `test_validate_pair_market_snapshot_missing_required` | Champ requis manquant → erreur |
| 4 | `test_validate_pair_market_snapshot_wrong_type` | Mauvais type → erreur |
| 5 | `test_dc_writer_validates_before_write` | Writer valide via schema_validator |
| 6 | `test_dc_writer_writes_manifest` | Manifest écrit via manifest_writer |
| 7 | `test_dc_writer_invalid_payload_raises` | Payload invalide → ValueError |
| 8 | `test_dc_writer_producer_path` | latest.json dans le bon producer path |

## Commande de vérification

```bash
python3 -m pytest tests/data_center -q           # 24 + nouveaux PASS
python3 -m pytest modules/collector_binance_spot/tests -q  # 7 PASS
python3 -m pytest modules/data_center/tests/test_spot_snapshot_dc_writer.py -q  # 10 PASS
```
