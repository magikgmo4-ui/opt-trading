---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01
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
  - PF_DATA_CENTER
  - PF_DESK_PRO
  - PF_OPENCLAW_ORCHESTRATOR_FULL
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/VALIDATION_RULES.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01/
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01/10_COLUMNS_CONTRACTS.md
---

# 00_INITIAL_PROJECT_DOC — Google Sheets API Write Adapter V1

## Objectif

Implémenter la couche d'écriture Google Sheets contrôlée pour le schéma global.

**Aucun appel Google API par défaut.** L'écriture réelle nécessite :
- Flag explicite `ALLOW_GOOGLE_SHEETS_API_WRITE=1`
- `spreadsheet_id` configuré
- Credentials ADC/service account (hors scope de ce GO)

## Contexte validé

`GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01` (PR #809) a livré :
- 11 fixtures JSONL pour tous les tabs canoniques
- Validateur R1-R10 (41 tests PASS)
- Zéro appel Google API

## Ce GO livre

| Fichier | Rôle |
|---|---|
| `modules/google_sheets_global_schema/validator.py` | Shared validator R1-R10 (extrait du test pour réutilisation) |
| `modules/google_sheets_global_schema/fake_sheets_client.py` | Fake in-memory client (tests sans API) |
| `modules/google_sheets_global_schema/sheets_writer.py` | Writer adapter contrôlé (3 modes) |
| `tests/test_google_sheets_api_write.py` | Tests writer + fake client (36 tests) |
| `tests/test_google_sheets_no_api_calls.py` | Tests isolation Google API (5 tests) |

## Modes d'écriture

| Mode | Quand | Comportement |
|---|---|---|
| `fake` | client = FakeSheetsClient() | Écriture in-memory, toujours autorisée |
| `dry_run` | dry_run=True (défaut) ou client=None | ok=True, rows_written=0, aucun appel API |
| `controlled_write` | dry_run=False + ALLOW_GOOGLE_SHEETS_API_WRITE=1 + spreadsheet_id | Écriture réelle (credentials requises séparément) |

## Règle canonique respectée

- Data Center = source normalisée. Sheets = consumer/export.
- Validation R1-R10 appliquée AVANT tout write (y compris fake).
- Aucun secret dans le code, les logs, ou le repo.

## NE PAS FAIRE

- Appeler Google Sheets API par défaut
- Écrire des credentials dans le repo
- Modifier `.env`
- Faire de Sheets une source canonique trading
- Câbler datasheet_writer ou learning_feeder runtime dans ce GO
