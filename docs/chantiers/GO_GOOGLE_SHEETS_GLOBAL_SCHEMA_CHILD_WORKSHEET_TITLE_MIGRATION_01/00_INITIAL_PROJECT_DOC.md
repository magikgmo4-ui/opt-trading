---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
pf_id: PF_GOOGLE_SHEETS_CONSUMER
status: open
lifecycle_stage: implementation
surface: modules/google_sheets_global_schema
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
upstream:
  - PF_GOOGLE_SHEETS_CONSUMER
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01/
  - modules/google_sheets_global_schema/sheets_writer.py
---

# 00_INITIAL_PROJECT_DOC — Worksheet Title Migration V1

## Problème

Un spreadsheet Google Sheets réel peut avoir des titres de worksheets qui ne correspondent pas aux noms canoniques :
- `Sheet1` (défaut Google, locale anglaise) au lieu de `daily_sessions`
- `Feuille 1` (locale française) au lieu de `daily_sessions`
- Tabs non-encore créés pour les 10 autres tabs canoniques

`CANONICAL_SHEETS.md` note explicitement : *"worksheet title à aligner sur `daily_sessions`"*.

## Objectif

Livrer un `WorksheetMigrator` qui :
1. **Audite** les titres de worksheets existants dans un spreadsheet
2. **Planifie** les renames (legacy → canonique) et créations (nouveaux tabs)
3. **Applique** le plan (avec flag + client réel, ou FakeSheetsClient en test)

**Aucun appel Google Sheets API réel par défaut.** Dry-run par défaut.

## Contexte validé

- **PR #813** : SheetsWriter + FakeSheetsClient + shared validator
- `LEGACY_TITLE_MAP` : "Sheet1" / "sheet1" / "Feuille 1" / "Feuille1" → `daily_sessions`
- Tabs canoniques (11) : définis dans `validator.CANONICAL_TABS`
- Extra worksheets (hors CANONICAL_TABS) : ignorés — jamais supprimés

## Ce GO livre

| Fichier | Rôle |
|---|---|
| `modules/google_sheets_global_schema/worksheet_migrator.py` | WorksheetMigrator : audit + plan + apply |
| `tests/test_google_sheets_worksheet_migrator.py` | 31 tests couvrant plan, apply, dry-run, fake, real-blocked, isolation API |

## Règles canoniques

- Dry-run par défaut (`dry_run=True`)
- Apply réel : `ALLOW_GOOGLE_SHEETS_API_WRITE=1` + `spreadsheet_id` requis
- Extra worksheets non canoniques : jamais supprimés
- FakeSheetsClient : simule rename via create (suffisant pour prouver la logique)
- Aucun secret dans le code, les logs, ou le repo

## NE PAS FAIRE

- Supprimer des worksheets non canoniques
- Appeler Google Sheets API sans flag explicite
- Modifier `sync_daily_session.py` dans ce GO
- Modifier `fake_sheets_client.py`, `sheets_writer.py` ou `validator.py`
