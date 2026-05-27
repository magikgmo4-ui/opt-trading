---
doc_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: open
lifecycle_stage: implementation
surface: modules/datasheet_writer
source_kind: canonical
created_at: 2026-05-26
updated_at: 2026-05-26
upstream:
  - PF_GOOGLE_SHEETS_CONSUMER
  - PF_OPENCLAW_ORCHESTRATOR_FULL
links:
  - docs/chantiers/GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01/
  - modules/google_sheets_global_schema/sheets_writer.py
  - modules/result_tracker/app/schema.py
---

# 00_INITIAL_PROJECT_DOC — DatasheetWriter Sheets Adapter V1

## Objectif

Câbler `DatasheetWriter` → `SheetsWriter` : après avoir écrit le `TradeRecord` en JSONL/CSV local, le résultat peut optionnellement être exporté vers le tab Google Sheets `strategy_events`.

## Flux

```
ResultTracker.track(req) -> TradeRecord
  -> DatasheetWriter.write(record)       # JSONL + CSV local (existant)
  -> write_trade_to_sheets(record, writer, payload_ref=jsonl_path)  # nouveau
     -> map_trade_to_event_row()
     -> SheetsWriter.write_rows("strategy_events", [row])
     -> WriteResult -> SheetsAdapterResult
```

## Mapping TradeRecord → strategy_events

| TradeRecord | strategy_events |
|---|---|
| `trade_id` | `event_id` |
| `"trade_result.v1"` | `event_type` |
| `closed_at` (+00:00 → Z) | `event_ts` |
| `ticker` | `ticker` |
| `outcome` | `outcome` |
| `net_pnl` | `net_pnl` |
| `jsonl_path` (optionnel) | `payload_ref` |

`event_ts` est normalisé depuis `+00:00` vers `Z` (format exigé par R1-R10).

## Contexte validé

- **PR #813** : SheetsWriter + FakeSheetsClient + shared validator
- `strategy_events` schema : `required=[event_id, event_type, event_ts]`, `pk=[event_id]`, `ref_cols=[payload_ref]`
- `DatasheetWriter` : écrit JSONL/CSV, aucun lien Sheets jusqu'ici
- `ResultTracker.track()` produit `TradeRecord` avec `closed_at` au format `+00:00`

## Ce GO livre

| Fichier | Rôle |
|---|---|
| `modules/datasheet_writer/app/sheets_adapter.py` | `map_trade_to_event_row()` + `write_trade_to_sheets()` |
| `modules/datasheet_writer/tests/test_sheets_adapter.py` | 22 tests adapter |

## Règles canoniques

- Sheets = consumer/export. `DatasheetWriter` local = source primaire.
- Validation R1-R10 appliquée par `SheetsWriter` avant tout write.
- Dry-run par défaut via `SheetsWriter.mode`.
- Aucun appel Google API sans `ALLOW_GOOGLE_SHEETS_API_WRITE=1`.
- `write_trade_to_sheets()` est optionnel — le caller décide d'injecter ou non un `SheetsWriter`.

## NE PAS FAIRE

- Modifier `DatasheetWriter.write()` pour forcer un appel Sheets
- Appeler Google Sheets API sans flag explicite
- Modifier `result_tracker`, `sheets_writer`, `validator`, `fake_sheets_client`
