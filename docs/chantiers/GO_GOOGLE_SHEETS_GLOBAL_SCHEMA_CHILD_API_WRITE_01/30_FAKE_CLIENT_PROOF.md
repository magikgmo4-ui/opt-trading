---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01_FAKE_CLIENT_PROOF
doc_type: proof_of_concept
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 30_FAKE_CLIENT_PROOF — Preuve FakeSheetsClient

## Résultats tests

```
tests/test_google_sheets_api_write.py   36 tests PASS, 0 FAIL
tests/test_google_sheets_no_api_calls.py  5 tests PASS, 0 FAIL
Total : 41 tests PASS
```

## Couverture par classe

| Classe | Tests | Description |
|---|---|---|
| TestFakeClientBasics | 6 | add_worksheet, retrieve, append, clear, write_records, reset |
| TestFakeWriterAllTabs | 11 | Un test par tab canonique — fixture PASS via fake client |
| TestWriterValidationGates | 8 | Inconnu, colonne manquante, enum invalide, ts invalide, PK dupliqué, ref_payload, validate=False, champs WriteResult |
| TestDryRunMode | 3 | dry_run ok=True, rows_written=0, mode property |
| TestRealClientBlocked | 3 | Sans flag → ok=False, sans spreadsheet_id → ok=False, mode no_client |
| TestEnsureWorksheet | 3 | create, inconnu, no_client |
| TestClearAndWrite | 2 | replace data, validate avant clear |
| TestNoGoogleModulesLoaded | 3 | import validator/fake_client/sheets_writer — 0 google.* |
| TestFakeClientNoNetwork | 2 | write 11 tabs + validate 11 tabs — 0 google.* après |

## Preuve isolation Google API

```
sys.modules avant import : {}
sys.modules après : {} (delta vide)
Google modules trouvés : set()
```

Les trois modules s'importent, le writer écrit tous les 11 tabs, et le validateur traite tous les 11 tabs — sans jamais charger `google`, `gspread`, `googleapiclient`, `google.auth`, ou `google.oauth2`.

## Preuve dry-run

```python
writer = SheetsWriter(client=None, dry_run=True)
result = writer.append_rows("watchlists", rows)
# result.ok = True
# result.mode = "dry_run"
# result.rows_written = 0
# result.rows_attempted = 3
```

## Preuve real-client bloqué

```python
os.environ.pop("ALLOW_GOOGLE_SHEETS_API_WRITE", None)
writer = SheetsWriter(client=_MockRealClient(), spreadsheet_id="dummy_id", dry_run=False)
result = writer.append_rows("watchlists", rows)
# result.ok = False
# result.error = "Real write blocked — set ALLOW_GOOGLE_SHEETS_API_WRITE=1 to enable"
# _MockRealClient.worksheet() never called
```

## Commande de vérification

```bash
python3 -m pytest tests/test_google_sheets_api_write.py tests/test_google_sheets_no_api_calls.py -v
```
