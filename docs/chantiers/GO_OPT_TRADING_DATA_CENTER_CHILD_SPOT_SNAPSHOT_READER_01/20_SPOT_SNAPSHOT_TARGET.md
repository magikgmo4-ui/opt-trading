---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01_TARGET
doc_type: target_spec
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01
created_at: 2026-05-25
---

# 20_SPOT_SNAPSHOT_TARGET

## Flux cible

```
collector_binance_spot normalize_pair_market_snapshot()
  │
  ▼
write_spot_snapshot_to_data_center(payload, root, update_registry)
  ├── data/data_center/spot/collector_binance_spot/latest.json   ← producer path
  ├── write_pair_market_snapshot_view(payload, root)
  │     ├── data/data_center/views/pair_market_snapshot/latest.json
  │     └── data/data_center/views/pair_market_snapshot/by_symbol/<SYM>.json
  └── update_producer_last_write("collector_binance_spot", ...)  ← runtime registry
```

## Règle canonique respectée

```
data/data_center/<family>/<producer_id>/  = écriture producer / audit
data/data_center/views/<contract_class>/  = lecture consumer
data/data_center/_registry/              = runtime state
```

## Reader Desk Pro

```python
read_spot_snapshot(path=None) -> Optional[dict]
```

- Lit depuis `data/data_center/views/pair_market_snapshot/latest.json`
- `entity_type != "pair_market_snapshot"` → `None`
- Absent/malformé → `None`
- Jamais d'appel API

## Invariants

- `update_registry=False` disponible pour les tests (évite de polluer tmpdir).
- Registry statique (`modules/data_center/registry/`) jamais muté.
- Tous les writes sont atomiques via tempfile + replace.
