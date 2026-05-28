# 10_CONTRACT_TEST_PLAN

## test_producer_contracts.py

| Test | Description |
|---|---|
| `test_producer_id_required` | Chaque producer doit avoir un `id` non vide |
| `test_producer_schema_required` | Chaque producer doit référencer un schéma existant |
| `test_producer_status_valid` | Status = `active` | `inactive` | `deprecated` |
| `test_producer_last_write_iso` | `last_write` est ISO8601 valide |

## test_consumer_contracts.py

| Test | Description |
|---|---|
| `test_consumer_id_required` | Chaque consumer doit avoir un `id` non vide |
| `test_consumer_reads_not_empty` | `reads[]` ne doit pas être vide |
| `test_consumer_schema_exists` | Chaque entrée dans `reads[]` correspond à un schéma connu |
| `test_consumer_status_valid` | Status = `active` | `inactive` |
| `test_consumer_last_read_iso` | `last_read` est ISO8601 valide |

## test_schema_normalization.py

| Test | Description |
|---|---|
| `test_market_metrics_schema` | Valide contre `market_metrics.v1` |
| `test_oi_schema` | Valide contre `oi.v1` |
| `test_funding_schema` | Valide contre `funding.v1` |
| `test_liquidations_schema` | Valide contre `liquidations.v1` |
| `test_long_short_schema` | Valide contre `long_short.v1` |
| `test_signal_schema` | Valide contre `signal.v1` |
| `test_event_schema` | Valide contre `event.v1` |

## test_registry_layout.py

| Test | Description |
|---|---|
| `test_layout_dirs_exist` | raw/, normalized/, cache/by_symbol/ existent |
| `test_registry_producers_format` | producers.json conforme |
| `test_registry_consumers_format` | consumers.json conforme |
| `test_manifest_required_fields` | `manifest.json` contient les champs obligatoires |
