# 10_IMPLEMENTATION_SPEC

## Layout manager (`storage/layout_manager.py`)

- Créer `data/data_center/<producer>/raw/`
- Créer `data/data_center/<producer>/normalized/`
- Créer `data/data_center/<producer>/cache/by_symbol/`
- Écrire `latest.json`, `manifest.json`, `status.json`, `events.jsonl`, `errors.jsonl`

## Registry manager (`storage/registry_manager.py`)

- Lire/écrire `data/data_center/_registry/producers.json`
- Lire/écrire `data/data_center/_registry/consumers.json`
- Lire/écrire `data/data_center/_registry/schema_versions.json`

## Manifest writer (`storage/manifest_writer.py`)

- Écrire `manifest.json` avec producer_id, schema, timestamp, status

## Schema validator (`validation/schema_validator.py`)

- Valider des blobs JSON contre les schémas canoniques (market_metrics.v1, oi.v1, etc.)
- Retourner `(valid: bool, errors: list[str])`
