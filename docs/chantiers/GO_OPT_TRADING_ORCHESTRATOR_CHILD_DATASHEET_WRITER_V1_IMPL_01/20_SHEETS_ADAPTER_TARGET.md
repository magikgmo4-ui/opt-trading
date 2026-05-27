---
doc_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01_SHEETS_ADAPTER_TARGET
doc_type: target_design
repo: opt-trading
go_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01
status: active
source_kind: canonical
updated_at: 2026-05-26
---

# 20_SHEETS_ADAPTER_TARGET — Design sheets_adapter V1

## Module livré

### `modules/datasheet_writer/app/sheets_adapter.py`

```python
@dataclass
class SheetsAdapterResult:
    ok: bool
    rows_written: int
    mode: str    # "fake" | "dry_run" | "controlled_write"
    error: str | None

def _to_iso_utc_z(ts: str) -> str:
    """Normalize +00:00 suffix to Z."""

def map_trade_to_event_row(record: TradeRecord, payload_ref: str = "") -> dict:
    """TradeRecord -> strategy_events row dict."""

def write_trade_to_sheets(
    record: TradeRecord,
    writer: SheetsWriter,
    payload_ref: str = "",
) -> SheetsAdapterResult:
    """Write TradeRecord to strategy_events via SheetsWriter."""
```

## Mapping détaillé

```
TradeRecord                    strategy_events row
─────────────────────────────────────────────────
trade_id                    -> event_id
"trade_result.v1" (const)   -> event_type
closed_at (+00:00 → Z)      -> event_ts         [timestamp validated R1-R10]
ticker                      -> ticker            [extra col, not in required]
outcome                     -> outcome           [extra col]
net_pnl                     -> net_pnl          [extra col]
payload_ref (arg, default "") -> payload_ref     [ref_col, R8-safe]
```

## Normalisation timestamp

```python
"2026-05-25T10:02:00+00:00"  ->  "2026-05-25T10:02:00Z"   # ResultTracker format
"2026-05-25T10:02:00Z"       ->  "2026-05-25T10:02:00Z"   # already correct
```

## Utilisation en orchestrateur

```python
# Après DatasheetWriter.write() :
dw_result = DatasheetWriter(output_dir).write(record, dry_run=False)
sheets_result = write_trade_to_sheets(
    record,
    writer=SheetsWriter(client=FakeSheetsClient()),  # ou writer réel
    payload_ref=dw_result.jsonl_path,
)
```

## Contrat de sécurité

- `write_trade_to_sheets` est une fonction standalone — le caller l'invoque optionnellement
- `DatasheetWriter.write()` non modifié (pas de side-effect Sheets implicite)
- Validation R1-R10 par `SheetsWriter` avant write (aucune donnée invalide envoyée)
- `payload_ref` = chemin JSONL relatif ou vide — jamais un payload JSON inline (R8-safe)
