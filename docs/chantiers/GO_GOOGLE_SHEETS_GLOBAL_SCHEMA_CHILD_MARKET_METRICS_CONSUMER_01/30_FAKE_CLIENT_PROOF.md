---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01_FAKE_CLIENT_PROOF
doc_type: proof_of_concept
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 30_FAKE_CLIENT_PROOF — Preuve consumer avec FakeSheetsClient

## Résultats tests

```
tests/test_google_sheets_market_metrics_consumer.py  21 tests PASS, 0 FAIL

Suite complète tests/test_google_sheets*.py          103 tests PASS, 0 FAIL
```

## Couverture par classe

| Classe | Tests | Description |
|---|---|---|
| TestMapMmV1ToRows | 9 | required cols, symbol, as_of, source_ref, null skip, not-collectable skip, row count, empty, R8 safe |
| TestMappedRowsValidation | 3 | 0 FAIL R1-R10, ISO UTC format, no duplicate PK |
| TestConsumerFakeClient | 3 | writes ok, rows_written=2, FakeSheetsClient records write |
| TestConsumerNoSource | 3 | absent file, wrong input_class, corrupt JSON → no_source |
| TestConsumerDryRun | 1 | dry_run ok=True, rows_written=0, rows_attempted>0 |
| TestNoGoogleApiCalls | 2 | import consumer + write via fake → 0 google.* modules |

## Preuve mapping

```python
payload = {
    "input_class": "market_metrics.v1",
    "symbol": "BTCUSDT",
    "metrics_ts": "2026-05-25T09:00:00Z",
    "provider_coverage": {"collectable_metrics": ["open_interest", "funding_rate"]},
    "metrics": {"open_interest": 18500000000.0, "funding_rate": 0.0001, "volume_futures": None},
}
rows = map_mm_v1_to_rows(payload, "data/data_center/views/market_metrics/latest.json")
# -> 2 rows (volume_futures skipped: None)
# rows[0] = {"as_of": "2026-05-25T09:00:00Z", "symbol": "BTCUSDT",
#             "metric_name": "open_interest", "value": 18500000000.0,
#             "source_ref": "data/data_center/views/market_metrics/latest.json"}
```

## Preuve no-op

```python
result = write_market_metrics_to_sheets(writer, source_path=Path("/nonexistent.json"))
# result.ok = True
# result.rows_written = 0
# result.mode = "no_source"
# result.error = None
```

## Commande de vérification

```bash
python3 -m pytest tests/test_google_sheets_market_metrics_consumer.py -v
python3 -m pytest tests/test_google_sheets*.py -q
```
