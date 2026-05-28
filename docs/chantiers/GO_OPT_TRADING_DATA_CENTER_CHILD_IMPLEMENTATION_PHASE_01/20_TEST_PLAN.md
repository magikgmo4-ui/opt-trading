# 20_TEST_PLAN

## Tests unitaires

```bash
python3 -m pytest tests/data_center/ -v
```

| Test | Cible |
|---|---|
| `test_layout_manager_create` | Création structure répertoires |
| `test_registry_manager_read_write` | Registry producers/consumers |
| `test_manifest_writer` | Écriture manifest.json |
| `test_schema_validator_valid` | Validation positive |
| `test_schema_validator_invalid` | Rejet blob invalide |
