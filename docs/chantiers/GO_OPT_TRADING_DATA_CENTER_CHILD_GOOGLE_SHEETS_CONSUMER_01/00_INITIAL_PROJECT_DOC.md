---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
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
links:
  - modules/data_center/registry/consumers.json
  - modules/data_center/google_sheets_market_reporting_consumer.py
  - modules/data_center/tests/test_google_sheets_market_reporting_consumer.py
  - modules/data_center/tests/test_contract_tests.py
  - modules/google_sheets_global_schema/market_metrics_consumer.py
  - modules/google_sheets_global_schema/sheets_writer.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01

## Objet

Rattacher le consumer Google Sheets à la logique Data Center normalisée (PF_DATA_CENTER) :

```
producer -> data/data_center/views/<contract_class>/... -> consumer
```

Ici, la surface cible est `PF_GOOGLE_SHEETS_CONSUMER` (export / reporting), pour la classe
de contrat `market_metrics.v1`.

## Décision structurante

- Le consumer “market_metrics → Sheets tab market_metrics” existe déjà dans le parent Google Sheets.
- Ce GO Data Center ne refait pas ce consumer, mais fournit le **wiring Data Center**
  (contrat + registry + fallback + tests) pour `google_sheets__market_reporting`.

## Ce que ce GO ne fait PAS

- Pas d’appel Google Sheets API réel (pas de credentials, pas de spreadsheet_id, pas de write live).
- Pas de cron/scheduler/orchestrateur.
- Pas de multi-symbol (`by_symbol/`) : le consumer reste `latest_only`.
- Ne rouvre pas le parent Google Sheets.
- Ne ferme pas PF_DATA_CENTER.

## BUNDLE_TARGET

- [x] `consumers.json`: `google_sheets__market_reporting` → `implemented`, `validated_at` renseigné
- [x] Consumer Data Center (wrapper) avec `fallback: error` effectif (raise si source absente)
- [x] Tests no-api (FakeSheetsClient) + tests de contrat mis à jour
