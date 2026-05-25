---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01
parent_go_id: GO_DESKPRO_INPUT_EXPANSION_01
status: open
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DESK_PRO
MASTER_PROJECT_PLAN_ID: MPP_DESKPRO_INPUT_EXPANSION
PARENT_GO_ID: GO_DESKPRO_INPUT_EXPANSION_01
BUNDLE_TARGET: MARKET_METRICS_READONLY_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - desk_pro
  - market_metrics
  - read_only
  - fixtures
  - dry_run
links:
  - modules/desk_pro/dry_run.py
  - modules/desk_pro/service/market_metrics_reader.py
  - tests/test_desk_pro_dry_run.py
  - tests/test_desk_pro_market_metrics_reader.py
  - tests/fixtures/admin_trading_contract_smoke/market_metrics_v1_minimal.json
---

# GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01

## Objet

Fermer le gap `market_metrics.v1` côté Desk Pro en read-only / fixtures-first.

`read_market_metrics()` existait déjà et lisait depuis DC view. Ce GO matérialise
la consommation dans `dry_run.py` et prouve la chaîne fixture → reader → synthèse.

## Ce que ce GO ne fait PAS

- Ne crée pas de collector live.
- Ne modifie pas les producers DC.
- Ne câble pas Coinglass.
- Ne crée pas de pipeline Telegram.

## 6_FINAL_TARGET

- `dry_run.py` : paramètre `market_metrics: list | None = None` dans `build_desk_pro_dry_run_synthesis()`, `run_desk_pro_dry_run()`, `validate_desk_pro_dry_run_inputs()`
- `summary.market_metrics_present` dans le résultat de synthèse
- Warning non bloquant : `"market_metrics missing: market-context-free synthesis"`
- Fixture `tests/fixtures/admin_trading_contract_smoke/market_metrics_v1_minimal.json`
- Tests : +5 dry_run + 4 reader = 9 nouveaux tests

## 12_INVARIANTS

- Absence de market_metrics = WARN, jamais FAIL.
- Aucun appel API live.
- PF_DATA_CENTER non modifié.
- Registry DC non modifié.

## BUNDLE_TARGET — MARKET_METRICS_READONLY_V1

- [x] Fixture `market_metrics_v1_minimal.json` créée
- [x] `dry_run.py` — `market_metrics` param + `market_metrics_present` dans summary
- [x] `_validate_market_metrics()` — warning non bloquant
- [x] 5 nouveaux tests `test_desk_pro_dry_run.py`
- [x] 4 nouveaux tests `test_desk_pro_market_metrics_reader.py` (fixture proof)
- [x] **90/90 PASS** (82 existants + 8 nouveaux sur suites ciblées)
