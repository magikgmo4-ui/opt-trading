---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01_EXISTING_SURFACE_READ
doc_type: surface_read
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01
created_at: 2026-05-25
---

# 10_EXISTING_SURFACE_READ

## État pré-GO

### collector_binance_spot

- Entrypoint : `modules/collector_binance_spot/src/collector_binance_spot/run.py`
- Output actuel : `modules/collector_binance_spot/outputs/latest.json` (local module)
- Format normalisé : `normalize_pair_market_snapshot()` → `entity_type: pair_market_snapshot`
- Champs : `contract_version`, `schema_version`, `module_id`, `provider_id`, `run_id`,
  `generated_at`, `entity_type`, `records[]` avec `pair_symbol`, `last_price`, `trading_status`, etc.
- **GAP-P03** : le collector écrit dans son module, PAS dans `data/data_center/spot/`

### pair_snapshot_view_writer.py

- `write_pair_market_snapshot_view(payload, root)` — existe déjà
- Écrit vers :
  - `data/data_center/views/pair_market_snapshot/latest.json`
  - `data/data_center/views/pair_market_snapshot/by_symbol/<SYM>.json`
- Valide `entity_type == "pair_market_snapshot"`
- Tests complets existants (87 PASS avant ce GO)

### Desk Pro spot_snapshot consumer

- `consumers.json` : `desk_pro__spot_snapshot = not_started`
- Aucun reader `spot_snapshot_reader.py` avant ce GO

### runtime_registry

- `update_producer_last_write()` — fonctionnel depuis GO_PRODUCER_WRITE_VALIDATION_01
- `collector_binance_spot` déclaré dans static registry, `last_write: null`

## Conclusion

Le pont entre collector et DC était manquant. Ce GO crée `spot_snapshot_dc_writer.py`
comme bridge + `spot_snapshot_reader.py` comme consumer Desk Pro read-only.
