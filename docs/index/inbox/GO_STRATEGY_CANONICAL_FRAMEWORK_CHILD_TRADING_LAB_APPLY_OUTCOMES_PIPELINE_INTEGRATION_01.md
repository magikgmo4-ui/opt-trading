---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_APPLY_OUTCOMES_PIPELINE_INTEGRATION_01
status: DONE
verdict: PASS_TRADING_LAB_APPLY_OUTCOMES_PIPELINE_INTEGRATION_01
pr: 871
merge_commit: 7aecf785
---

Pipeline lab complet en une commande. `run-with-outcomes` : clear → batch_run → apply_outcomes → batch_report. `batch-run` implémenté (était dans usage string, absent de COMMANDS). 13 tests intégration PASS. Résultat : 10 sessions → 6W/4L/0T avg_r=0.8.

## delivered

- `batch_run()` — itère toutes les sessions × dates disponibles du CSV
- `run_with_outcomes()` — pipeline atomique en une commande
- `test_pipeline_integration_v1.py` — 13 tests PASS (idempotence, outcome fields, session filter)

## result

- 13 tests intégration PASS
- run-with-outcomes: 10 sessions → 6W/4L/0T avg_r=0.8
- idempotence vérifiée

## remaining_gap

- Pipeline validé sur données synthétiques (sample real-like 92 rows)
- Mesure réelle requiert données broker depuis state/trading_lab_v1/inputs/xauusd_m1_broker_<date>.csv
- Prochaine étape : GO_TRADING_LAB_REAL_BROKER_MEASUREMENT_01
