---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01_FIXTURE_PROOF
doc_type: fixture_proof
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01
created_at: 2026-05-25
---

# 30_FIXTURE_FIRST_PROOF

## Payload fixture

Fixture inline dans les tests (BTCUSDT, entity_type pair_market_snapshot, 1 record) :
```json
{
  "contract_version": "v1", "schema_version": "v1",
  "module_id": "collector_binance_spot", "provider_id": "binance_spot",
  "run_id": "20260525_000000_test", "generated_at": "2026-05-25T00:00:00Z",
  "entity_type": "pair_market_snapshot",
  "records": [{"pair_symbol": "BTCUSDT", "last_price": "67800.00", "trading_status": "TRADING"}]
}
```

## Chaîne de preuve

```
fixture payload
  → write_spot_snapshot_to_data_center(payload, root=tmp, update_registry=False)
     → data/data_center/spot/collector_binance_spot/latest.json  ✅
     → data/data_center/views/pair_market_snapshot/latest.json   ✅
     → data/data_center/views/pair_market_snapshot/by_symbol/BTCUSDT.json  ✅
  → read_spot_snapshot(path=view_latest)
     → entity_type == "pair_market_snapshot" ✅
     → records present ✅
  → update_registry=True → runtime registry updated ✅
```

## Tests — résultats

### `modules/data_center/tests/test_spot_snapshot_dc_writer.py` — 10 tests

| Test | Vérification |
|------|-------------|
| `test_writes_producer_path` | fichier producer créé |
| `test_producer_path_contains_payload` | entity_type + records corrects |
| `test_writes_consumer_view_latest` | view latest créée |
| `test_writes_consumer_view_by_symbol` | by_symbol/BTCUSDT.json créé |
| `test_returns_dict_with_paths` | retour contient producer_latest, view_latest, by_symbol |
| `test_runtime_registry_updated_when_enabled` | collector_binance_spot last_write non-null |
| `test_runtime_registry_skipped_when_disabled` | registry non écrit si update_registry=False |
| `test_static_registry_not_mutated` | static registry inchangé |
| `test_raises_on_wrong_entity_type` | ValueError si entity_type incorrect |
| `test_two_records_written_to_by_symbol` | 2 by_symbol files pour BTCUSDT + ETHUSDT |

### `tests/test_desk_pro_spot_snapshot_reader.py` — 8 tests

| Test | Vérification |
|------|-------------|
| `test_reads_valid_payload` | retourne dict non-null |
| `test_has_correct_entity_type` | entity_type == "pair_market_snapshot" |
| `test_has_records` | records non vide |
| `test_returns_none_if_file_absent` | None si inexistant |
| `test_returns_none_if_wrong_entity_type` | None si entity_type incorrect |
| `test_returns_none_if_malformed_json` | None si JSON invalide |
| `test_returns_none_if_not_dict` | None si liste JSON |
| `test_never_raises` | aucune exception propagée |

## Verdict

**105 PASS (97 DC suite + 8 reader) — PASS.**
