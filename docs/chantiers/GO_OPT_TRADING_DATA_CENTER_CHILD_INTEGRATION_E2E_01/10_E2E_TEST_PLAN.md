# 10_E2E_TEST_PLAN

## Pipeline

```text
Producer (mock) → raw/ → normalized/ → latest.json → registry → consumer (mock)
```

## Tests

| Test | Description |
|---|---|
| `test_pipeline_producer_to_normalized` | Producer mock écrit raw → normalisation |
| `test_pipeline_normalized_to_registry` | Normalized → registry producers.json |
| `test_pipeline_registry_to_consumer` | Consumer mock lit du registry |
| `test_pipeline_schema_validation` | Blob invalide → erreur dans errors.jsonl |
| `test_pipeline_full_cycle` | Cycle complet avec 3 producers simulés |
