---
doc_id: GO_OPT_TRADING_SECURITY_CREDENTIALS_GOOGLE_ADC_FIX_01_INIT
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_SECURITY_CREDENTIALS_GOOGLE_ADC_FIX_01
status: DONE
created_at: 2026-06-03
---

# Fix — Google Sheets credentials registry (ADC regression)

## Contexte

PR #501 avait validé la méthode ADC (Application Default Credentials) pour Google Sheets :
- Auth : `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/spreadsheets`
- Variable : `GOOGLE_SHEETS_SYNC_SHEET_ID`
- Pas de fichier JSON service account

Le chantier `GO_OPT_TRADING_LOCALCMS_CREDENTIALS_PANEL_01` (PR #1085) a introduit une régression :
- `GOOGLE_SERVICE_ACCOUNT_JSON_PATH` ajouté dans le registre — incorrect (méthode service account abandonnée)
- `GOOGLE_SHEETS_SPREADSHEET_ID` utilisé au lieu de `GOOGLE_SHEETS_SYNC_SHEET_ID` — mauvais nom

## Fichiers modifiés

| Fichier | Changement |
|---------|-----------|
| `configs/env/registry/credentials.yaml` | Suppression `google_service_account_json` + renommage `GOOGLE_SHEETS_SPREADSHEET_ID` → `GOOGLE_SHEETS_SYNC_SHEET_ID` |
| `modules/localcms/app/main.py` | `_CREDS` : idem, -1 entrée Google (34 total) |
| `scripts/credentials_form.py` | `CREDS` : idem, -1 entrée Google (34 total) |

## Verdict

```text
REGRESSION = CORRECTED
GOOGLE_AUTH_METHOD = ADC (gcloud auth application-default login)
GOOGLE_SHEETS_ENV_VAR = GOOGLE_SHEETS_SYNC_SHEET_ID
SERVICE_ACCOUNT_JSON = NOT_REQUIRED (supprimé du registre)
TOTAL_CREDENTIALS = 34 (était 35)
UNKNOWN = 0
```
