---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01_TARGET
doc_type: post_gate_dry_run_target
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01
status: closed
created_at: 2026-05-26
---

# 20_POST_GATE_DRY_RUN_TARGET — Cible et changements

## Fichiers modifiés

### `scripts/e2e/dry_run_pipeline.py`

**Ajouts** :
1. Constantes de flags (après DRY_RUN/PAPER_MODE) :
   ```python
   ALLOW_E2E_LIVE_DRY_RUN = os.environ.get("ALLOW_E2E_LIVE_DRY_RUN", "0") == "1"
   ALLOW_LIVE_TRADE = os.environ.get("ALLOW_LIVE_TRADE", "0") == "1"
   ALLOW_GOOGLE_SHEETS_API_WRITE = os.environ.get("ALLOW_GOOGLE_SHEETS_API_WRITE", "0") == "1"
   ALLOW_TELEGRAM_SEND = os.environ.get("ALLOW_TELEGRAM_SEND", "0") == "1"
   ```

2. Fonction `_preflight_post_gate()` :
   - BLOCKED si `ALLOW_E2E_LIVE_DRY_RUN != "1"`
   - BLOCKED si `DRY_RUN` env var pas explicitement "1"
   - BLOCKED si `ALLOW_LIVE_TRADE=1` présent

3. Appel preflight au début de `main()` — retour immédiat BLOCKED si échec.

4. Variable `_gate_status_label` initialisée à `"NONE"`, mise à `"APPROVED_PAPER"` en step 3.

5. Bloc `e2e_post_gate_status` à la fin de `main()` :
   ```json
   {
     "status": "PASS",
     "dry_run": true,
     "live_trade": false,
     "gate_status": "APPROVED_PAPER",
     "localcms_gate": "WARN_SKIPPED",
     "sheets_mode": "fake",
     "telegram_mode": "dry_run",
     "modules": {
       "signal_router": "PASS",
       "proposition_engine": "PASS",
       "validation_gate": "PASS",
       "trade_executor": "PASS",
       "result_tracker": "PASS",
       "datasheet_writer": "PASS",
       "learning_feeder": "PASS"
     }
   }
   ```

6. Pipeline name mis à jour : `"E2E post-gate live/dry-run"`

7. `__main__` exit : vérifie `e2e_post_gate_status.status == "BLOCKED"` → rc=1.

### `scripts/e2e/daily_session_journal.py`

`_run_pipeline()` injecte les flags manquants via `os.environ.setdefault()` :
```python
os.environ.setdefault("ALLOW_E2E_LIVE_DRY_RUN", "1")
os.environ.setdefault("DRY_RUN", "1")
```

### `tests/e2e/test_e2e_dry_run_pipeline.py`

Tous les appels subprocess mis à jour :
- `"ALLOW_E2E_LIVE_DRY_RUN": "1"` ajouté aux envs
- `test_dry_run_env_default` : `DRY_RUN=1` rendu explicite
- Assertions `report["pipeline"]` mises à jour vers `"E2E post-gate live/dry-run"`

### `tests/e2e/test_dry_run_pipeline_localcms_gate.py`

`_run()` mis à jour :
- `"ALLOW_E2E_LIVE_DRY_RUN": "1"` dans le base env
- `env.pop("ALLOW_LIVE_TRADE", None)` ajouté

## Fichier créé

`tests/e2e/test_e2e_live_dry_run_post_gate.py` — 40 tests, 7 classes :

| Classe | Tests | Couverture |
|--------|-------|------------|
| TestPreflightFlags | 7 | BLOCKED sur flags manquants/interdits |
| TestPostGatePipelineSuccess | 16 | Chaîne complète PASS avec flags corrects |
| TestLocalcmsGateBehavior | 3 | default/require/skip modes |
| TestGateRejectionBlocksTradeExecutor | 3 | Gate obligatoire avant trade |
| TestFakeSheetsIntegration | 3 | payload_ref, fake mode, no google |
| TestLearningFeederDryRun | 2 | bridge_status=dry_run, no brick |
| TestNoExternalCalls | 6 | aucun appel externe prouvé |

## Commandes de run

```bash
# Mode nominal
ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/dry_run_pipeline.py

# Mode strict LocalCMS (BLOCKED si absent)
ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 REQUIRE_LOCALCMS_E2E=1 python3 scripts/e2e/dry_run_pipeline.py || true

# BLOCKED — sans flag
python3 scripts/e2e/dry_run_pipeline.py  # rc=1, e2e_post_gate_status.status=BLOCKED
```
