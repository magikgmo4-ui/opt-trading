---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01_REPRISE
doc_type: reprise_point
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01
status: closed
created_at: 2026-05-26
---

# 90_REPRISE_POINT

## État au closeout

GO fermé. Aucun travail en suspens.

## Branche

`go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01`

## Fichiers modifiés

- `scripts/e2e/dry_run_pipeline.py` — preflight, flags, e2e_post_gate_status
- `scripts/e2e/daily_session_journal.py` — injection flags
- `tests/e2e/test_e2e_dry_run_pipeline.py` — ALLOW_E2E_LIVE_DRY_RUN=1 dans tous les subprocess
- `tests/e2e/test_dry_run_pipeline_localcms_gate.py` — ALLOW_E2E_LIVE_DRY_RUN=1 dans _run()

## Fichier créé

- `tests/e2e/test_e2e_live_dry_run_post_gate.py` — 40 tests

## Pour reproduire le run E2E

```bash
# Run nominal
ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/dry_run_pipeline.py

# Run tests
python3 -m pytest tests/e2e/ -q

# Suite orchestrator complète
python3 -m unittest \
  modules.signal_router.tests.test_router \
  modules.proposition_engine.tests.test_proposition \
  modules.validation_gate.tests.test_gate \
  modules.trade_executor.tests.test_executor \
  modules.result_tracker.tests.test_tracker \
  modules.datasheet_writer.tests.test_writer \
  modules.learning_feeder.tests.test_feeder
```

## Invariants à maintenir

- `ALLOW_E2E_LIVE_DRY_RUN=1` toujours requis pour lancer le pipeline
- `DRY_RUN=1` toujours requis et explicite
- `ALLOW_LIVE_TRADE` doit rester absent
- Tous les dispatcher.dispatch() calls restent `dry_run=True`
- FakeSheetsClient par défaut pour Sheets
