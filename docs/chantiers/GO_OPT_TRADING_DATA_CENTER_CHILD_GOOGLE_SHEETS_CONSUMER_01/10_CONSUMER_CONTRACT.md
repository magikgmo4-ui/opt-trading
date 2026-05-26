---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01_CONSUMER_CONTRACT
doc_type: consumer_contract
repo: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
created_at: 2026-05-26
updated_at: 2026-05-26
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
SURFACE_LINK: PF_GOOGLE_SHEETS_CONSUMER
---

# 10_CONSUMER_CONTRACT — Google Sheets market reporting

## Identité

- consumer_id: `google_sheets__market_reporting`
- surface: `PF_GOOGLE_SHEETS_CONSUMER`
- contract_class: `market_metrics.v1`
- access_pattern: `latest_only`
- read_path: `data/data_center/views/market_metrics/latest.json`
- fallback: `error`

## Entrypoint runtime (repo)

- `modules/data_center/google_sheets_market_reporting_consumer.py`
  - `consume_google_sheets_market_reporting(writer, root=..., source_path=...)`

## Comportement contractuel

- La lecture DC est la source canonique (pas de fallback legacy).
- Si le fichier est absent ou invalide: **raise** (conforme `fallback: error`).
- Les écritures Sheets utilisent `SheetsWriter` :
  - `FakeSheetsClient` en tests (zéro API)
  - `dry_run` par défaut côté “real client”
  - `controlled_write` uniquement si activé explicitement (flag env + spreadsheet_id)
