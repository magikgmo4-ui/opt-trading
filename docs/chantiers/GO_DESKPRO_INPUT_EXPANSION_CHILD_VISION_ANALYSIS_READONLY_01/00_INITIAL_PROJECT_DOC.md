---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01
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
BUNDLE_TARGET: VISION_ANALYSIS_READONLY_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - desk_pro
  - vision_analysis
  - read_only
  - fixtures
  - dry_run
links:
  - modules/desk_pro/dry_run.py
  - modules/desk_pro/service/vision_analysis_reader.py
  - tests/test_desk_pro_dry_run.py
  - tests/test_desk_pro_vision_analysis_reader.py
  - tests/fixtures/admin_trading_contract_smoke/vision_analysis_v1_minimal.json
---

# GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01

## Objet

Fermer le gap `vision_analysis.v1` côté Desk Pro en read-only / fixtures-first.

Aucun reader `vision_analysis` n'existait dans le repo. Ce GO crée
`modules/desk_pro/service/vision_analysis_reader.py`, matérialise la consommation
dans `dry_run.py`, et prouve la chaîne fixture → reader → synthèse.

## Ce que ce GO ne fait PAS

- Ne crée pas de bot vision live.
- Ne fait pas d'OCR ni d'analyse d'image.
- Ne câble pas Playwright / headless.
- Ne modifie pas PF_DATA_CENTER.
- Ne crée pas de pipeline Telegram.

## 6_FINAL_TARGET

- `modules/desk_pro/service/vision_analysis_reader.py` : `read_vision_analysis(path=None) -> Optional[dict]`
- `dry_run.py` : paramètre `vision_analysis: dict | None = None` dans `build_desk_pro_dry_run_synthesis()`, `run_desk_pro_dry_run()`, `validate_desk_pro_dry_run_inputs()`
- `summary.vision_analysis_present` dans le résultat de synthèse
- Warning non bloquant : `"vision_analysis missing: vision-context-free synthesis"`
- Fixture `tests/fixtures/admin_trading_contract_smoke/vision_analysis_v1_minimal.json`
- Tests : +4 dry_run + 10 reader = 14 nouveaux tests

## 12_INVARIANTS

- Absence de vision_analysis = WARN, jamais FAIL.
- Aucun appel API, OCR, browser, modèle vision.
- PF_DATA_CENTER non modifié.

## BUNDLE_TARGET — VISION_ANALYSIS_READONLY_V1

- [x] Fixture `vision_analysis_v1_minimal.json` créée (BTCUSDT H1, 3 signaux)
- [x] `vision_analysis_reader.py` — `read_vision_analysis()` read-only
- [x] `dry_run.py` — `vision_analysis` param + `vision_analysis_present` dans summary
- [x] `_validate_vision_analysis()` — warning non bloquant
- [x] 4 nouveaux tests `test_desk_pro_dry_run.py`
- [x] 10 nouveaux tests `test_desk_pro_vision_analysis_reader.py`
- [x] **63/63 PASS** sur suites ciblées
