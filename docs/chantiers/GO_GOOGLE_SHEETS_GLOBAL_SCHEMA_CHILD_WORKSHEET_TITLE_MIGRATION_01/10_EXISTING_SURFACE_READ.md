---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01_EXISTING_SURFACE_READ
doc_type: existing_surface_read
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 10_EXISTING_SURFACE_READ — Surfaces existantes

## Problème documenté

`CANONICAL_SHEETS.md` — colonne `migration_notes` :
```
daily_sessions | worksheet title à aligner sur `daily_sessions`
```

`scripts/sheets/sync_daily_session.py` écrit sur `sheet1` :
```python
sheet = client.open_by_key(sheet_id).sheet1
```

Le premier onglet d'un nouveau Google Sheets s'appelle "Sheet1" (locale anglaise) ou "Feuille 1" (locale française). Le script écrit dessus sans renommer.

## Titres legacy connus

| Titre legacy | Locale | Canonique cible |
|---|---|---|
| `Sheet1` | Anglais (défaut) | `daily_sessions` |
| `sheet1` | — | `daily_sessions` |
| `Feuille 1` | Français | `daily_sessions` |
| `Feuille1` | Français (variante) | `daily_sessions` |
| `Hoja 1` | Espagnol | `daily_sessions` |
| `Tabelle1` | Allemand | `daily_sessions` |

Seul `daily_sessions` est concerné par un rename. Les 10 autres tabs canoniques n'existent pas encore dans les spreadsheets réels → action `create`.

## SheetsWriter disponible (PR #813)

`SheetsWriter.ensure_worksheet(sheet_name)` crée un worksheet si absent. Le migrator complète cette logique en gérant les renames de titres existants.

## Interface gspread utilisée

```python
# audit
spreadsheet.worksheets()          # list[gspread.Worksheet]
ws.title                          # str

# rename
ws = spreadsheet.worksheet(title) # gspread.Worksheet
ws.update_title(new_title)        # str -> None

# create
spreadsheet.add_worksheet(title, rows, cols)
```

`FakeSheetsClient` supporte déjà :
- `worksheets_created: list[str]` ← utilisé pour `audit()`
- `add_worksheet(*, title)` ← utilisé pour `create` (et simule `rename` en test)
