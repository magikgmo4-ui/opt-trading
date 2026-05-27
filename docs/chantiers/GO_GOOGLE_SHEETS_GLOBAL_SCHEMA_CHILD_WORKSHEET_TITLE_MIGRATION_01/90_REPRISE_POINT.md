---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 90_REPRISE_POINT — Point de reprise

## État livré

| Fichier | Status |
|---|---|
| `modules/google_sheets_global_schema/worksheet_migrator.py` | CRÉÉ |
| `tests/test_google_sheets_worksheet_migrator.py` | CRÉÉ — 31 tests PASS |
| `docs/chantiers/GO_.../00_INITIAL_PROJECT_DOC.md` | CRÉÉ |
| `docs/chantiers/GO_.../10_EXISTING_SURFACE_READ.md` | CRÉÉ |
| `docs/chantiers/GO_.../20_MIGRATOR_TARGET.md` | CRÉÉ |
| `docs/chantiers/GO_.../30_FAKE_CLIENT_PROOF.md` | CRÉÉ |
| `docs/chantiers/GO_.../40_GAPS_AND_NEXT_GO.md` | CRÉÉ |
| `docs/chantiers/GO_.../90_REPRISE_POINT.md` | CE FICHIER |
| `docs/index/inbox/GO_...01.md` | CRÉÉ |
| `FILE_SCOPE.txt` | CRÉÉ |

## Validation locale

```bash
python3 -m pytest tests/test_google_sheets_worksheet_migrator.py -v
# 31 tests PASS, 0 FAIL

python3 -m pytest tests/test_google_sheets*.py -q
# 134 tests PASS, 0 FAIL
```

## Commande de reprise

```bash
python3 -c "
from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
from modules.google_sheets_global_schema.worksheet_migrator import WorksheetMigrator

client = FakeSheetsClient()
client.add_worksheet(title='Sheet1')   # simule un spreadsheet réel
m = WorksheetMigrator(client=client)
result = m.run()
print('mode:', result.mode)
print('applied:', [str(a) for a in result.actions_applied])
print('canonical worksheets:', client.worksheets_created)
"
```

## Prochain GO immédiat

**GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01**
