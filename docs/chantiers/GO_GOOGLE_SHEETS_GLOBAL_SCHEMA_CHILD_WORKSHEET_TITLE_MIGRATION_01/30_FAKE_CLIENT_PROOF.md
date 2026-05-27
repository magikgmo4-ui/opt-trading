---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01_FAKE_CLIENT_PROOF
doc_type: proof_of_concept
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 30_FAKE_CLIENT_PROOF — Preuve WorksheetMigrator

## Résultats tests

```
tests/test_google_sheets_worksheet_migrator.py   31 tests PASS, 0 FAIL

Suite complète tests/test_google_sheets*.py      134 tests PASS, 0 FAIL
```

## Couverture par classe

| Classe | Tests | Description |
|---|---|---|
| TestMigrationPlan | 12 | empty→11 creates, Sheet1→rename, French locale, all ok, unknown ignored, canonical wins over legacy, plan count=11, covers all tabs, legacy consumed once |
| TestMigrationActionStr | 3 | __str__ readable pour ok/rename/create |
| TestMigratorDryRun | 3 | apply dry_run → no actions, run() no client → dry_run, mode property |
| TestMigratorFakeClient | 7 | 11 actions sur empty, all creates, Sheet1→rename, canonical worksheets créés, no migration needed, audit, mode |
| TestRealClientBlocked | 4 | sans flag → blocked, sans spreadsheet_id → blocked, dry_run=True+flag → pas appliqué, audit mock |
| TestNoGoogleApiCalls | 2 | import + run fake → 0 google.* |

## Preuve plan Sheet1

```python
m = WorksheetMigrator()
plan = m.plan(["Sheet1"])
# plan.renames = 1
# plan.creates = 10
# plan.already_ok = 0
# renames[0] = MigrationAction("rename", "daily_sessions", current_title="Sheet1")
```

## Preuve run() fake empty

```python
client = FakeSheetsClient()
m = WorksheetMigrator(client=client)
result = m.run()
# result.ok = True
# result.mode = "fake"
# len(result.actions_applied) = 11
# all action.action == "create"
# set(client.worksheets_created) ⊇ CANONICAL_TABS
```

## Commande de vérification

```bash
python3 -m pytest tests/test_google_sheets_worksheet_migrator.py -v
python3 -m pytest tests/test_google_sheets*.py -q
```
