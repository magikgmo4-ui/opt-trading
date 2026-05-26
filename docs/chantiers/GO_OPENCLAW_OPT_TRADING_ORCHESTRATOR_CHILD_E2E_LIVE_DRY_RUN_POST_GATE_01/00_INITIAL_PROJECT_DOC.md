---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01_INITIAL
doc_type: initial_project_doc
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: active
created_at: 2026-05-26
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01

## Objectif

Préparer et prouver un run E2E post-gate papier en mode live/dry-run contrôlé.

Chaîne cible :
```
signal_router → proposition_engine → validation_gate → trade_executor
→ result_tracker → datasheet_writer → learning_feeder
```

## Mode live/dry-run

"live/dry-run" = environnement semi-réel, composants appelés bout-en-bout, gate papier explicite, `dry_run=True`, aucun ordre réel, aucune API externe obligatoire.

## Invariants absolus

- NO_LIVE_TRADE_WITHOUT_GATE
- dry_run=True obligatoire
- Aucun ordre exchange réel
- Aucun secret requis par défaut
- Google Sheets = FakeSheetsClient par défaut
- Telegram = dry_run par défaut
- LocalCMS = optional gate par défaut

## Flags

| Flag | Valeur | Effet |
|------|--------|-------|
| ALLOW_E2E_LIVE_DRY_RUN | 1 | Autorise le mode post-gate (obligatoire) |
| DRY_RUN | 1 | Obligatoire ; si absent → BLOCKED |
| ALLOW_LIVE_TRADE | absent | Si présent → BLOCKED |
| REQUIRE_LOCALCMS_E2E | 1 | LocalCMS absent → BLOCKED |
| SKIP_LOCALCMS_E2E | 1 | Skip LocalCMS check |

## Contexte

- #830 : parent acceptance review PASS
- #834 : Sheets integration test PASS (46/46)
- #839 : LocalCMS E2E gate PASS (51/51)
- #843 : requests gap CLOSED (27/27)
- Gap restant : pas de run E2E post-gate prouvé avec flags explicites
