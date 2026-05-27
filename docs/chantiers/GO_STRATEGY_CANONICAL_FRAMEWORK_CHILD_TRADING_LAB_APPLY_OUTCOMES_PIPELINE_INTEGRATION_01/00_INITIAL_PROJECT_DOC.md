---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_APPLY_OUTCOMES_PIPELINE_INTEGRATION_01
status: CLOSED
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
---

# GO: Apply Outcomes Pipeline Integration

## Objectif

Intégrer le moteur `apply_outcomes` au pipeline complet `trading_lab_v1` afin qu'un run de lab produise automatiquement des trades avec `result`, `exit_price`, `exit_ts`, `bars_held`, `outcome_reason` et `r_realized` sans étape manuelle séparée.

## Gap avant ce GO

- `apply-outcomes` existait en CLI, mais restait une étape manuelle post-run.
- `batch-run` était référencé dans le message d'usage mais non implémenté dans COMMANDS.
- Aucune commande unique ne produisait un batch report enrichi en un shot.

## Livrables

- `batch_run(args)` — itère toutes les sessions activées × toutes les dates disponibles du CSV
- `run_with_outcomes(args)` — pipeline atomique : clear state → batch_run → apply_outcomes → batch_report
- `test_pipeline_integration_v1.py` — 13 tests d'intégration (TestRunWithOutcomes + TestBatchRun)
