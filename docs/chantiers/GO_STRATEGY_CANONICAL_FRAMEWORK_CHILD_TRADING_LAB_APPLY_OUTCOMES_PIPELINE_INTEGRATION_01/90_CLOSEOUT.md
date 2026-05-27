---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_APPLY_OUTCOMES_PIPELINE_INTEGRATION_01
doc_type: closeout
status: CLOSED
---

# Closeout

## Résultat de validation

- `test_pipeline_integration_v1.py` : 13/13 tests PASS
- Intégration : `run-with-outcomes` → 10 sessions → 6W/4L/0T avg_r=0.8
- Suite complète trading_lab_v1 : 91/94 PASS (3 pre-existing param_sweep failures)
- `tests/test_strategy_adapter.py` : 27/27 PASS
- `validate_strategy_registry.py` : WARNINGS seulement (pre-existing)

## Décision de conception

`run_with_outcomes` efface l'état avant de run (clear semantics) pour garantir l'idempotence. Le clear est nécessaire car `batch_run` est additif (append). Une alternative "merge" a été écartée pour sa complexité.

## Commandes disponibles après ce GO

```bash
python3 -c "from modules.trading_lab_v1.app.trading_lab_v1 import run_with_outcomes; run_with_outcomes([])"
# ou
python3 modules/trading_lab_v1/app/trading_lab_v1.py run-with-outcomes
python3 modules/trading_lab_v1/app/trading_lab_v1.py batch-run [csv_path] [session_id]
```

## Remaining gap

- Pipeline validé sur données synthétiques (sample real-like)
- Mesure réelle requiert données broker depuis `state/trading_lab_v1/inputs/xauusd_m1_broker_<date>.csv`
- Prochaine étape : `GO_TRADING_LAB_REAL_BROKER_MEASUREMENT_01`
