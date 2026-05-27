---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01_GAPS_AND_NEXT_GO
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 40_GAPS_AND_NEXT_GO — Lacunes et prochains GOs

## Ce GO ne livre pas

| Hors scope | Raison |
|---|---|
| Credentials ADC / service account | Hors scope volontaire — gestion des secrets séparée |
| Runtime wiring datasheet_writer | GO dédié : GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01 |
| Runtime wiring learning_feeder | GO dédié : GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_IMPL_01 |
| Consumer market_metrics réel | GO dédié : GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01 |
| Migration worksheet title (tab renaming) | GO dédié : GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01 |
| Header row management | `_rows_to_values()` ne gère pas les headers — à câbler par le consumer |
| Retry / backoff sur erreurs Google API | Délégué à gspread ou au wrapper consumer |
| Batch write multi-tab atomique | Non requis à ce stade |

## État des dépendances

| Dépendance | Status |
|---|---|
| `gspread` | Optionnel — non installé par défaut ; le writer s'importe sans |
| `google.auth` | Optionnel — idem |
| ADC (`gcloud auth application-default login`) | Opérationnel (patron validé dans `sync_daily_session.py`) |

## Prochains GOs (ordre logique)

1. **GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01** — consumer market_metrics : lit depuis Data Center, écrit via SheetsWriter
2. **GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01** — migration des titres de worksheets (renommage canonique)
3. **GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01** — câblage datasheet_writer → SheetsWriter runtime
4. **GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_IMPL_01** — câblage learning_feeder → SheetsWriter runtime

## Lacunes connues non bloquantes

- `_rows_to_values()` convertit toutes les valeurs en `str` — les consumers doivent s'assurer que le type de colonne est accepté par Sheets (nombres, dates).
- `get_or_create_worksheet` sur client réel fait un appel réseau même en dry_run si appelé directement via `ensure_worksheet`. À isoler si nécessaire.
- `FakeSheetsWorksheet.get_all_records()` reconstruit les dicts sans header row — utilisation interne seulement.
