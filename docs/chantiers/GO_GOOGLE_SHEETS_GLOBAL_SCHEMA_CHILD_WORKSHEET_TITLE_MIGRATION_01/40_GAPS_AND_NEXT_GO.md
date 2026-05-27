---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01_GAPS_AND_NEXT_GO
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 40_GAPS_AND_NEXT_GO — Lacunes et prochains GOs

## Ce GO ne livre pas

| Hors scope | Raison |
|---|---|
| Appel réel Google Sheets API | Credentials + spreadsheet_id à configurer séparément |
| Suppression de worksheets non canoniques | Décision volontaire — trop destructif sans inventaire préalable |
| Mise à jour de `sync_daily_session.py` pour utiliser le migrator | GO dédié ou maintenance script |
| Script CLI d'exécution du migrator | GO dédié runner |
| Détection automatique de `spreadsheet_id` | Hors scope — fourni par l'opérateur |
| Migration de contenu (copier données de Sheet1 dans daily_sessions) | Non nécessaire — daily_sessions est append-only |

## Lacunes connues non bloquantes

- Le fake client simule `rename` via `add_worksheet(canonical)` — l'ancien titre legacy reste dans le fake store. Acceptable : les tests vérifient la logique de plan/apply, pas la fidélité du rename in-memory.
- `LEGACY_TITLE_MAP` ne couvre que `daily_sessions`. Si d'autres tabs acquièrent des titres legacy, étendre la map dans un GO suivant.
- Le migrator lit les worksheets via `client.worksheets()` — si la gspread Spreadsheet object n'expose pas cette interface (e.g., utilisation d'un `Client` plutôt qu'un `Spreadsheet`), adapter l'appelant.

## Prochains GOs

1. **GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01** — câblage datasheet_writer → SheetsWriter runtime
2. **GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_IMPL_01** — câblage learning_feeder → SheetsWriter runtime
