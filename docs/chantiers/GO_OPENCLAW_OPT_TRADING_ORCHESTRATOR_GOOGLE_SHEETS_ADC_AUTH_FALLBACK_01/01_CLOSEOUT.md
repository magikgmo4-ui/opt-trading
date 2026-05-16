# ADC Auth Fallback — Closeout

## Decision

```
JSON key (GOOGLE_SHEETS_CREDENTIALS_JSON) = BLOCKED by iam.disableServiceAccountKeyCreation
ADC (Application Default Credentials)     = NEW default auth method
```

## Changes

### sync_daily_session.py

| Before (JSON key)                           | After (ADC)                                      |
| ------------------------------------------- | ------------------------------------------------ |
| `ServiceAccountCredentials.from_json_keyfile_dict()` | `google.auth.default(scopes=[...])`         |
| Required: `GOOGLE_SHEETS_CREDENTIALS_JSON`  | Not required                                     |
| Required: `GOOGLE_SHEETS_SYNC_SHEET_ID`     | Required (unchanged)                             |
| Error: `failed_no_credentials`              | Error: `BLOCKED_AUTH_ADC`                        |
| Hint: set `GOOGLE_SHEETS_CREDENTIALS_JSON`  | Hint: `gcloud auth application-default login`    |

### Tests

All 26 existing tests pass with the new auth flow.

## Setup machine

```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/spreadsheets

export GOOGLE_SHEETS_SYNC_SHEET_ID="1hFUfz2R7RqkV4xUaCM-mtYNfSQ4OZ1YBN_inexg-X4k"
```

## Verification

- Dry-run: works without any credentials ✅
- Controlled-write without ADC: `BLOCKED_AUTH_ADC` with setup instructions ✅

## Test results

- 26/26 `test_sync_daily_session.py` — PASS
- 17/17 `test_daily_session_journal.py` — PASS
- 17/17 `test_daily_session_journal_html.py` — PASS

## Contraintes

- Aucun JSON secret dans le repo ✅
- Aucun secret dans les logs ✅
- Controlled-write manuel uniquement ✅
- No live trade / No Bitget order ✅
- LocalCMS read-only ✅
