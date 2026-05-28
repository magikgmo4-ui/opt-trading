# 10_CONTRACTS_SPEC

## Producer contracts

### market_metrics.v1 (référence)

```
Schéma : défini dans GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
Format : JSON
Producteur : derivatives_collector, collector_binance_spot
Consommateur : Desk Pro
```

### Contrat producer — format canonique

```json
{
  "producer_id": "string",
  "schema_version": "string",
  "produced_at": "ISO8601",
  "data": {},
  "metadata": {
    "source": "string",
    "symbol": "string | null",
    "interval": "string | null",
    "quality": "LIVE|SIMULATED|BACKFILL"
  }
}
```

### Layout stockage

```text
data/data_center/
  <producer_id>/
    raw/
    normalized/
    latest.json
    manifest.json
    status.json
```

## Module structure

```text
modules/data_center/
  contracts/
    __init__.py
    producer_registry.py
    contract_validator.py
    market_metrics_v1.py
  tests/
    test_producer_registry.py
    test_contract_validator.py
```
