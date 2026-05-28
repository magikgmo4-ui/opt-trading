---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01_IMPLEMENTATION_SPEC
doc_type: implementation_spec
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01
created_at: 2026-05-28
---

# 10_IMPLEMENTATION_SPEC

## 1. Schéma market_metrics.v1

Mise à jour dans `modules/data_center/schemas/registry.py` :

```python
MARKET_METRICS_V1 = _make_spec(
    required_fields=[
        "schema", "input_class", "contract_version", "module_id", "symbol",
        "metrics_ts", "freshness_state", "provider_coverage", "metrics", "refs",
    ],
    field_types={
        "schema": str,
        "input_class": str,
        "contract_version": str,
        "module_id": str,
        "symbol": str,
        "metrics_ts": str,
        "freshness_state": str,
        "provider_coverage": dict,
        "metrics": dict,
        "refs": dict,
    },
)
```

## 2. enrich_produced_at()

Nouvelle fonction publique dans `market_metrics_writer.py` :

```python
def enrich_produced_at(payload, override_timestamp=None):
    """Tag a MarketMetricsV1 payload with produced_at + schema fields.

    Returns a dict with schema: "market_metrics.v1" and produced_at set
    to the current UTC ISO timestamp (or override_timestamp if provided).
    Accepts MarketMetricsV1 dataclass or dict.
    """
```

Appelée par `write_market_metrics_to_data_center()` si `schema` pas encore présent.

## 3. Validation + manifest dans DC writer

`write_market_metrics_to_data_center()` :
1. `enrich_produced_at()` si `schema` manquant
2. `validate_blob()` contre `market_metrics.v1`
3. `_validate_input_class()` (préservé)
4. Écriture `latest.json` + `by_symbol` (existant)
5. `write_manifest()` via Data Center manifest_writer
6. `update_producer_last_write()` (existant)

## 4. Tests

Nouveaux tests dans `tests/derivatives_collector/test_market_metrics_writer_dc_alignment.py` :

| Test | Objet |
|------|-------|
| `test_enrich_produced_at_adds_schema` | `schema: "market_metrics.v1"` ajouté |
| `test_enrich_produced_at_adds_timestamp` | `produced_at` ISO timestamp |
| `test_enrich_produced_at_override` | override_timestamp fonctionne |
| `test_enrich_produced_at_accepts_dataclass` | Accepte MarketMetricsV1 |
| `test_enrich_produced_at_accepts_dict` | Accepte dict |
| `test_dc_writer_validates_schema` | validation passe sur payload enrichi |
| `test_dc_writer_writes_manifest` | manifest.json écrit avec bons champs |
| `test_dc_writer_invalid_payload_raises` | payload invalide → ValueError |
