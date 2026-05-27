---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_TELEGRAM_CLAIM_READONLY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_TELEGRAM_CLAIM_READONLY_01
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
BUNDLE_TARGET: TELEGRAM_CLAIM_READONLY_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - desk_pro
  - telegram_claim
  - read_only
  - fixtures
  - dry_run
links:
  - modules/desk_pro/dry_run.py
  - modules/desk_pro/service/telegram_claim_reader.py
  - tests/test_desk_pro_dry_run.py
  - tests/test_desk_pro_telegram_claim_reader.py
  - tests/fixtures/admin_trading_contract_smoke/telegram_claim_v1_minimal.json
---

# GO_DESKPRO_INPUT_EXPANSION_CHILD_TELEGRAM_CLAIM_READONLY_01

## Objet

Fermer le gap `telegram_claim.v1` côté Desk Pro en read-only / fixtures-first.

Aucun reader `telegram_claim` n'existait dans le repo. Ce GO crée
`modules/desk_pro/service/telegram_claim_reader.py`, matérialise la consommation
dans `dry_run.py`, et prouve la chaîne fixture → reader → synthèse.

## Ce que ce GO ne fait PAS

- Ne crée pas de bot Telegram.
- N'envoie aucun message Telegram.
- Ne lit aucun channel live.
- Ne crée pas de screener Telegram.
- Ne modifie pas PF_DATA_CENTER.

## 6_FINAL_TARGET

- `modules/desk_pro/service/telegram_claim_reader.py` : `read_telegram_claim(path=None) -> Optional[dict]`
- `dry_run.py` : paramètre `telegram_claim: dict | None = None` dans `build_desk_pro_dry_run_synthesis()`, `run_desk_pro_dry_run()`, `validate_desk_pro_dry_run_inputs()`
- `summary.telegram_claim_present` dans le résultat de synthèse
- Warning non bloquant : `"telegram_claim missing: telegram-context-free synthesis"`
- Fixture `tests/fixtures/admin_trading_contract_smoke/telegram_claim_v1_minimal.json`
- Tests : +4 dry_run + 10 reader = 14 nouveaux tests

## 12_INVARIANTS

- Absence de telegram_claim = WARN, jamais FAIL.
- Aucun appel API Telegram.
- Aucune lecture channel live.
- Aucun envoi message.
- PF_DATA_CENTER non modifié.

## BUNDLE_TARGET — TELEGRAM_CLAIM_READONLY_V1

- [x] Fixture `telegram_claim_v1_minimal.json` créée (BTCUSDT H1, claim trade_context)
- [x] `telegram_claim_reader.py` — `read_telegram_claim()` read-only
- [x] `dry_run.py` — `telegram_claim` param + `telegram_claim_present` dans summary
- [x] `_validate_telegram_claim()` — warning non bloquant
- [x] 4 nouveaux tests `test_desk_pro_dry_run.py`
- [x] 10 nouveaux tests `test_desk_pro_telegram_claim_reader.py`
- [x] **77/77 PASS** sur suites ciblées
