---
doc_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01
status: active
source_kind: canonical
updated_at: 2026-05-26
---

# 90_REPRISE_POINT — Point de reprise

## État livré

| Fichier | Status |
|---|---|
| `modules/datasheet_writer/app/sheets_adapter.py` | CRÉÉ |
| `modules/datasheet_writer/tests/test_sheets_adapter.py` | CRÉÉ — 22 tests PASS |
| Tous les docs chantier | CRÉÉS |
| `FILE_SCOPE.txt` | CRÉÉ |
| `docs/index/inbox/...md` | CRÉÉ |

## Validation locale

```bash
python3 -m pytest modules/datasheet_writer/tests/test_sheets_adapter.py -v
# 22 tests PASS

python3 -m pytest modules/datasheet_writer/tests/ tests/test_google_sheets*.py -q
# 169 tests PASS
```

## Commande de reprise

```python
from modules.result_tracker.app.schema import TradeRecord
from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
from modules.google_sheets_global_schema.sheets_writer import SheetsWriter
from modules.datasheet_writer.app.sheets_adapter import write_trade_to_sheets

record = TradeRecord(
    trade_id="paper_BTCUSDT_test",
    request_id="req-001", signal_id="sig-001",
    ticker="BTCUSDT", action="BUY",
    entry_price=65000.0, close_price=67000.0,
    fill_qty=0.5, size_pct=0.5,
    sl=63000.0, tp=70000.0,
    gross_pnl=1000.0, net_pnl=961.0, fees=39.0,
    duration_s=120.0, outcome="win",
    opened_at="2026-05-26T10:00:00+00:00",
    closed_at="2026-05-26T10:02:00+00:00",
    dry_run=True,
)
writer = SheetsWriter(client=FakeSheetsClient())
result = write_trade_to_sheets(record, writer, payload_ref="data/datasheet/trades_20260526.jsonl")
print(result)
```

## Prochain GO

**GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_IMPL_01**
