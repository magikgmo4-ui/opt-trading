---
doc_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01_FAKE_CLIENT_PROOF
doc_type: proof_of_concept
repo: opt-trading
go_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01
status: active
source_kind: canonical
updated_at: 2026-05-26
---

# 30_FAKE_CLIENT_PROOF — Preuve sheets_adapter

## Résultats tests

```
modules/datasheet_writer/tests/test_sheets_adapter.py   22 tests PASS, 0 FAIL

Régression (datasheet_writer + google_sheets suite)     169 tests PASS, 0 FAIL
```

## Couverture par classe

| Classe | Tests | Description |
|---|---|---|
| TestMapTradeToEventRow | 10 | required cols, event_id, event_type, +00:00→Z, Z inchangé, ticker/outcome/net_pnl, payload_ref vide, payload_ref path |
| TestMappedRowValidation | 4 | 0 FAIL R1-R10, ISO UTC, no duplicate PK, duplicate PK rejeté (R7) |
| TestWriteTradeToSheets | 6 | fake ok, rows_written=1, mode="fake", dry_run no_write, payload_ref forwarded, SheetsAdapterResult type |
| TestNoGoogleApiCalls | 2 | import + write fake → 0 google.* |

## Preuve mapping

```python
record = TradeRecord(
    trade_id="paper_BTCUSDT_abc123",
    closed_at="2026-05-25T10:02:00+00:00",
    ticker="BTCUSDT", outcome="win", net_pnl=961.0, ...
)
row = map_trade_to_event_row(record, payload_ref="data/datasheet/trades_20260525.jsonl")
# row = {
#   "event_id": "paper_BTCUSDT_abc123",
#   "event_type": "trade_result.v1",
#   "event_ts": "2026-05-25T10:02:00Z",   # +00:00 -> Z
#   "ticker": "BTCUSDT",
#   "outcome": "win",
#   "net_pnl": 961.0,
#   "payload_ref": "data/datasheet/trades_20260525.jsonl",
# }
# validate_rows("strategy_events", [row]) -> 0 FAIL
```

## Preuve write fake

```python
writer = SheetsWriter(client=FakeSheetsClient())
result = write_trade_to_sheets(record, writer)
# result.ok = True
# result.rows_written = 1
# result.mode = "fake"
# result.error = None
```

## Commande de vérification

```bash
python3 -m pytest modules/datasheet_writer/tests/test_sheets_adapter.py -v
python3 -m pytest modules/datasheet_writer/tests/ tests/test_google_sheets*.py -q
```
