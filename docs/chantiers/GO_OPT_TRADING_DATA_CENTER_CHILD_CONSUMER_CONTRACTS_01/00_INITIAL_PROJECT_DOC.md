---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
pf_id: PF_DATA_CENTER
status: open
lifecycle_stage: implementation
surface: modules/data_center
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
upstream:
  - GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01 — INITIAL_PROJECT_DOC

## Objectif

Définir et formaliser les contrats consumers du Data Center : format de lecture,
latence acceptable, endpoints ou paths d'accès, règles de fallback pour chaque
surface consommatrice.

## 1_MASTER_TARGET

```text
data/data_center/ -> consumer contract -> surface
```

Consommateurs identifiés :
- PF_DESK_PRO
- PF_STRATEGY_FRAMEWORK_REGISTRY
- PF_PERF_ENGINE_TRADING_LAB
- PF_TELEGRAM_SCREENER
- PF_TELEGRAM_INGESTION
- PF_GOOGLE_SHEETS_CONSUMER
- PF_LOCALCMS_COCKPIT

## 17_RESUME_POINT

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01
```
