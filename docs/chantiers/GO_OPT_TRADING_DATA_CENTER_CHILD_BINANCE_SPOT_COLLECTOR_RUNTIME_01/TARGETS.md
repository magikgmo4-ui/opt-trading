# TARGETS — BINANCE_SPOT_COLLECTOR_RUNTIME_V1

## Fichiers modifiés

| Fichier | Type | Description |
|---------|------|-------------|
| `modules/data_center/schemas/registry.py` | modified | Ajout schema `pair_market_snapshot.v1` |
| `modules/data_center/spot_snapshot_dc_writer.py` | modified | Validation schema + manifest_writer |
| `modules/collector_binance_spot/src/collector_binance_spot/run.py` | modified | Appel DC writer après normalisation |
| `modules/data_center/tests/test_spot_snapshot_dc_writer.py` | modified | Ajout `schema` dans payload test |
| `tests/data_center/test_binance_spot_dc_runtime.py` | new | 11 tests runtime DC pour binance_spot |
| `docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01/` | new | 5 docs chantier |

## Résumé des changements

1. **Registry** : `pair_market_snapshot.v1` registré comme 8e schéma canonique Data Center.
2. **DC Writer** : `write_spot_snapshot_to_data_center()` valide le payload via `schema_validator()` et écrit `manifest.json` via `manifest_writer()` avant l'écriture producer et view. Lève `ValueError` si validation échoue.
3. **Collector run** : Après succès de normalisation et écriture locale, `run_collection()` appelle `write_spot_snapshot_to_data_center()` avec le payload enrichi du champ `schema`. L'appel est encapsulé dans lazy import + try/except pour ne pas casser le run principal.
4. **Tests** : 11 nouveaux tests (schema registry, validation, DC writer, manifest, runtime registry) + tests existants mis à jour (ajout `schema` dans payload).

## Tests

```bash
python3 -m pytest tests/data_center -q           # 35/35 PASS (24 anciens + 11 nouveaux)
python3 -m pytest modules/collector_binance_spot/tests -q  # 7/7 PASS (hors 1 pre-existing failure sur sot/mainline)
python3 -m pytest modules/data_center/tests/test_spot_snapshot_dc_writer.py -q  # 10/10 PASS
```

## Vérification

- `pair_market_snapshot.v1` : registré, requiert `schema`, `contract_version`, `entity_type`, `records`
- `write_spot_snapshot_to_data_center()` : valide via `validate_blob` avant écriture
- `manifest.json` : écrit à `data/data_center/spot/collector_binance_spot/manifest.json`
- Runtime registry : mis à jour via `update_producer_last_write()`
- GAP-P03 résolu : collector écrit dans `data/data_center/spot/collector_binance_spot/`
