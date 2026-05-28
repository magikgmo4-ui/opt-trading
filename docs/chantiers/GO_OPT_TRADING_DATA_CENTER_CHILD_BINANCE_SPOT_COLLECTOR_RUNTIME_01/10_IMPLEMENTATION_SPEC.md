---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01_IMPLEMENTATION_SPEC
doc_type: implementation_spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01
status: open
created_at: 2026-05-28
updated_at: 2026-05-28
---

# 10_IMPLEMENTATION_SPEC

## 1. Schema pair_market_snapshot.v1

Ajout dans `modules/data_center/schemas/registry.py` :

```python
PAIR_MARKET_SNAPSHOT_V1 = _make_spec(
    required_fields=[
        "contract_version", "schema_version", "module_id", "provider_id",
        "run_id", "generated_at", "entity_type", "records",
    ],
    field_types={
        "contract_version": str,
        "schema_version": str,
        "module_id": str,
        "provider_id": str,
        "run_id": str,
        "generated_at": str,
        "entity_type": str,
        "records": list,
    },
)
register_schema("pair_market_snapshot.v1", PAIR_MARKET_SNAPSHOT_V1)
```

## 2. Amélioration spot_snapshot_dc_writer.py

Modifier `write_spot_snapshot_to_data_center()` pour :

1. Valider le payload entrant contre `pair_market_snapshot.v1` via `validate_blob()`.
2. Écrire `manifest.json` via `write_manifest()` du Data Center.
3. Lever `ValueError` si validation échoue (inchangé pour l'appelant).
4. Préserver signature exacte pour compatibilité.

La fonction étendue :
```python
def write_spot_snapshot_to_data_center(payload, root=None, update_registry=True):
    validate_blob(payload)  # nouveau — schema pair_market_snapshot.v1
    # write latest.json (existant)
    # write view (existant)
    # write manifest via write_manifest() (nouveau)
    # update registry (existant)
```

## 3. Câblage run.py

Dans `run_collection()`, après `atomic_write_json(config.paths.latest_path, latest)` (ligne ~148),
ajouter un appel conditionnel à `write_spot_snapshot_to_data_center()`.

La décision : écrire dans le Data Center uniquement si le module est configuré pour.
Pour la v1, on écrit toujours dans le DC après un run normalisé réussi, avec `update_registry=True`.

Modification minimale : après le bloc try où normalized_payload est produit,
insérer l'appel DC writer. En cas d'échec du DC writer, le run principal n'est pas
interrompu (log error, continue).

## 4. Tests

Nouveau fichier `tests/data_center/test_binance_spot_dc_runtime.py` :

| Test | Objet |
|------|-------|
| `test_schema_registered` | `pair_market_snapshot.v1` est dans le registry |
| `test_validate_valid_payload` | Un payload normalisé valide passe la validation |
| `test_validate_missing_field` | Un payload sans champ requis échoue |
| `test_dc_writer_validates` | `write_spot_snapshot_to_data_center` valide avant écriture |
| `test_dc_writer_writes_manifest` | `manifest.json` est écrit avec les bons champs |
| `test_dc_writer_invalid_raises` | Payload invalide → ValueError |
| `test_run_collection_calls_dc_writer` | `run_collection()` écrit bien dans le DC |
