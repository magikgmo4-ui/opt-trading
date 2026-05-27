---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_SHEETS_INTEGRATION_TEST_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_SHEETS_INTEGRATION_TEST_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: open
lifecycle_stage: opening
surface: modules/datasheet_writer
source_kind: canonical
updated_at: 2026-05-26
topic_keys:
  - orchestration
  - google-sheets
  - integration-test
  - datasheet-writer
---

# 00_INITIAL_PROJECT_DOC — Sheets Integration Test

## 1_MASTER_TARGET

Prouver le flux `ResultTracker → DatasheetWriter → SheetsAdapter (fake)` sans API réelle, en cohérence avec les GOs Sheets déjà mergés (`GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_*`).

## 2_INITIAL_PROJECT_DOC

Ce GO ferme le gap « Sheets adapter integration test futur » identifié dans `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01`.

## 3_INITIAL_NEED

`datasheet_writer/app/writer.py` et `sheets_adapter.py` sont deux composants séparés. Il n'existe pas de test qui prouve que la sortie du writer (JSONL + `payload_ref`) s'enchaîne correctement avec le Sheets adapter. De plus, les timestamps produits par `ResultTracker` incluent des microsecondes qui échouent la validation R5 (`YYYY-MM-DDTHH:MM:SSZ`).

## 4_CANONICAL_STATE_BEFORE

```text
sheets_adapter.py  : PASS (22 tests isolés)
test_writer.py     : PASS (13 tests isolés)
intégration R→DW→SA : ABSENT
_to_iso_utc_z()    : ne tronque pas les microsecondes → R5 FAIL si timestamp live
```

## 5_FINAL_TARGET

- `_to_iso_utc_z()` tronque les microsecondes (R5 PASS)
- `test_sheets_integration.py` — 11 tests : ResultTracker→SheetsAdapter + DatasheetWriter→SheetsAdapter + no-Google-API
- 46/46 PASS (13 writer + 22 adapter + 11 intégration)
