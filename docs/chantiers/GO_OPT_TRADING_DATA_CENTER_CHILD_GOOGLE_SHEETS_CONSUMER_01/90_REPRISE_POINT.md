---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01_REPRISE_POINT
doc_type: reprise_point
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

# 90_REPRISE_POINT — Reprise stable

## État établi

- `google_sheets__market_reporting` est déclaré `implemented` dans `modules/data_center/registry/consumers.json`.
- Un wrapper Data Center existe et applique `fallback: error` (raise si la source DC est absente/invalide).
- Tests “no API” valident l’écriture via `FakeSheetsClient`.

## Point de reprise

1. Si besoin, câbler un orchestrateur runtime (GO orchestrator) pour exécuter le consumer en `dry_run` / `controlled_write`.
2. Étendre ensuite la chaîne PF_DATA_CENTER côté producers (contrats + latence + storage) selon les close-gates du parent.
