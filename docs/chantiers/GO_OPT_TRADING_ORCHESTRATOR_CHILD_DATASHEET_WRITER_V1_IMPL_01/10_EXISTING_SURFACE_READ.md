---
doc_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01_EXISTING_SURFACE_READ
doc_type: existing_surface_read
repo: opt-trading
go_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01
status: active
source_kind: canonical
updated_at: 2026-05-26
---

# 10_EXISTING_SURFACE_READ — Surfaces existantes

## `modules/datasheet_writer/app/writer.py`

`DatasheetWriter.write(record: TradeRecord, dry_run: bool = True) -> WriteResult`

Écrit en JSONL + CSV dans `data/datasheet/trades_YYYYMMDD.{jsonl,csv}`. Retourne `WriteResult(ok, dry_run, written, jsonl_path, csv_path, error)`.

**Ce GO n'y touche pas** — la méthode `write()` n'est pas modifiée. L'adapter Sheets est une fonction séparée que le caller invoque optionnellement après `DatasheetWriter.write()`.

## `modules/result_tracker/app/schema.py`

```python
@dataclass
class TradeRecord:
    trade_id: str          # -> event_id
    closed_at: str         # ISO 8601, format +00:00 depuis ResultTracker.track()
    ticker: str
    outcome: str           # "win" | "loss" | "breakeven"
    net_pnl: float
    ...
```

`closed_at` utilise `datetime.fromtimestamp(..., tz=timezone.utc).isoformat()` → `"2026-05-25T10:02:00+00:00"`. Le validator R1-R10 exige `...Z`. L'adapter normalise via `_to_iso_utc_z()`.

## `modules/google_sheets_global_schema/validator.py` (PR #813)

```python
"strategy_events": {
    "required": ["event_id", "event_type", "event_ts"],
    "enums": {},
    "timestamps": ["event_ts"],
    "pk": ["event_id"],
    "ref_cols": ["payload_ref"],
}
```

Colonnes supplémentaires (`ticker`, `outcome`, `net_pnl`) : non définies dans `required` → acceptées par le validator sans FAIL.

## `modules/google_sheets_global_schema/sheets_writer.py` (PR #813)

`SheetsWriter.write_rows("strategy_events", rows) -> WriteResult`

Dry-run par défaut. Fake client autorisé sans flag.
