---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01_INDEX
doc_type: inbox_index
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01
parent_go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
pf_id: PF_GOOGLE_SHEETS_CONSUMER
status: open
lifecycle_stage: implementation
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
---

# GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01

**Objectif :** Aligner les titres de worksheets Google Sheets sur les noms canoniques (audit + plan + apply).

**Surface :** `modules/google_sheets_global_schema/worksheet_migrator.py`

**Parent :** GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01

## Livrables

| Fichier | Rôle |
|---|---|
| `modules/google_sheets_global_schema/worksheet_migrator.py` | WorksheetMigrator : audit / plan / apply |
| `tests/test_google_sheets_worksheet_migrator.py` | 31 tests |

## Résultat

31 tests PASS. 134 tests PASS suite complète. "Sheet1" → rename "daily_sessions". 10 autres tabs → create. Dry-run par défaut. Isolation API prouvée.

## Chantier docs

`docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01/`
