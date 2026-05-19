---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_ADC_AUTH_FALLBACK_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #495  (Controlled-write pilot — merged DEGRADED)
  - PR #496  (Credentials setup + retry plan — merged)
  - PR #497  (Controlled-write execution — merged BLOCKED)
  - PR #499  (External credentials setup — merged)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_ADC_AUTH_FALLBACK_01

## Objectif

Remplacer la dépendance à `GOOGLE_SHEETS_CREDENTIALS_JSON` (bloquée par
policy) par Application Default Credentials (ADC) via `google.auth.default()`.

## Décision

La clé JSON service account est bloquée par `iam.disableServiceAccountKeyCreation`.
On ne contourne pas la policy. Fallback : ADC.

## Changements

### sync_daily_session.py

- Remplacer `_try_get_sheets_client()` :
  ```python
  from google.auth import default
  import gspread
  credentials, project_id = default(scopes=[
      "https://www.googleapis.com/auth/spreadsheets"
  ])
  client = gspread.authorize(credentials)
  sheet = client.open_by_key(sheet_id).sheet1
  ```
- `GOOGLE_SHEETS_CREDENTIALS_JSON` n'est plus requis
- `GOOGLE_SHEETS_SYNC_SHEET_ID` reste requis (env var)
- Dry-run : fonctionne sans ADC ni SHEET_ID
- Controlled-write : nécessite ADC valide + SHEET_ID
- Message d'erreur : `BLOCKED_AUTH_ADC` si ADC absent en mode write

### Tests

- Ajuster les tests pour ne plus mocker `GOOGLE_SHEETS_CREDENTIALS_JSON`
- Mocker `google.auth.default()` pour les tests write

## Setup machine

```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/spreadsheets

export GOOGLE_SHEETS_SYNC_SHEET_ID="1hFUfz2R7RqkV4xUaCM-mtYNfSQ4OZ1YBN_inexg-X4k"
```

## Contraintes

- Aucun JSON secret dans le repo
- Aucun secret dans les logs
- Controlled-write manuel uniquement
- No live trade / No Bitget order
- LocalCMS read-only
