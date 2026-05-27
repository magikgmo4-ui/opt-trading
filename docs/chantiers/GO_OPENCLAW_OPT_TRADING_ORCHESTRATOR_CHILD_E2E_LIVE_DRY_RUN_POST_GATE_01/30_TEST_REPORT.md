---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01_TEST_REPORT
doc_type: test_report
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01
status: closed
verdict: PASS
created_at: 2026-05-26
---

# 30_TEST_REPORT — Résultats de validation

## Suite E2E globale

```
python3 -m pytest tests/e2e/ -q
154 passed in 10.67s
```

| Fichier | Tests | Résultat |
|---------|-------|----------|
| `test_e2e_dry_run_pipeline.py` | 23 | 23/23 PASS |
| `test_dry_run_pipeline_localcms_gate.py` | 28 | 28/28 PASS |
| `test_daily_session_journal.py` | 18 | 18/18 PASS |
| `test_e2e_live_dry_run_post_gate.py` (nouveau) | 40 | 40/40 PASS |
| autres (session, perf, telegram) | 45 | 45/45 PASS |
| **Total** | **154** | **ALL PASS** |

## Suite orchestrator modules

```
python3 -m unittest modules.{signal_router,proposition_engine,validation_gate,
                              trade_executor,result_tracker,datasheet_writer,
                              learning_feeder}.tests.*
156 tests — OK
```

## Détail `test_e2e_live_dry_run_post_gate.py` — 40 tests

### TestPreflightFlags (7)
- `test_blocked_without_allow_e2e_flag` : rc=1, BLOCKED ✓
- `test_blocked_when_dry_run_not_set` : rc=1, BLOCKED ✓
- `test_blocked_when_dry_run_false` : rc=1, BLOCKED ✓
- `test_blocked_when_allow_live_trade_set` : rc=1, BLOCKED ✓
- `test_blocked_report_has_all_fields` : tous les champs présents ✓
- `test_blocked_report_live_trade_false_without_flag` : live_trade=False ✓
- `test_blocked_report_live_trade_true_when_set` : live_trade=True ✓

### TestPostGatePipelineSuccess (16)
- exits_0, status=PASS, dry_run=True, live_trade=False ✓
- gate_status=APPROVED_PAPER ✓
- sheets_mode=fake, telegram_mode=dry_run ✓
- 7 modules PASS ✓
- trade_executor dry_run=True, datasheet_writer written=False ✓
- learning_feeder bridge_status=dry_run, brick_stored=False ✓

### TestLocalcmsGateBehavior (3)
- default absent → WARN_SKIPPED, rc=0, E2E continue ✓
- require absent → BLOCKED, rc=1 ✓
- skip → rc=0 ✓

### TestGateRejectionBlocksTradeExecutor (3)
- rejected gate → status=rejected ✓
- hold gate → status=rejected ✓
- approved gate + dry_run → status in (dry_run, filled) ✓

### TestFakeSheetsIntegration (3)
- fake sheets reçoit payload_ref → rows_written=1, mode=fake ✓
- aucun module google.oauth2 chargé ✓
- DatasheetWriter dry_run → written=False ✓

### TestLearningFeederDryRun (2)
- bridge_status=dry_run, brick_stored=False, dry_run=True ✓
- store_brick=True ignoré si dry_run=True ✓

### TestNoExternalCalls (6)
- pas de gspread/google.oauth2 dans le script ✓
- pas de send_telegram() direct ✓
- tous dispatcher.dispatch guarded by dry_run=True ✓
- pas de bitget ✓
- pas de create_order/place_order ✓
- aucun module google dans le rapport JSON ✓

## Scripts de validation

```bash
# E2E nominal
ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/dry_run_pipeline.py
# → rc=0, e2e_post_gate_status.status=PASS, gate_status=APPROVED_PAPER

# E2E strict LocalCMS
ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 REQUIRE_LOCALCMS_E2E=1 python3 scripts/e2e/dry_run_pipeline.py
# → rc=1, localcms_gate.status=BLOCKED, e2e_status=FAIL (LocalCMS absent)
```
