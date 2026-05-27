# 30 — Lifecycle / Promotion / Retirement Decision

## Décision par stratégie

| strategy_id | lifecycle actuel | Décision | Justification |
|---|---|---|---|
| `SMC_ICT_CHOCH_BOS_RETEST` | CANDIDATE | **Maintenir CANDIDATE** | Observation-only, `perf_status=UNMEASURED`, pas de runtime actif |
| `xau_session_open_v1` | CANDIDATE | **Maintenir CANDIDATE** | Actif sur `trading_realtime_v1` + `trading_lab_v1`, `perf_status=UNMEASURED` — promotion exige mesure perf |
| `COINM_SHORT` | CANDIDATE | **Maintenir CANDIDATE** | Actif sur surfaces P0 mais `perf_status=UNMEASURED` — promotion après mesure |
| `USDTM_LONG` | CANDIDATE | **Maintenir CANDIDATE** | `perf_status=UNMEASURED`, P1 |
| `GOLD_CFD_LONG` | CANDIDATE | **Maintenir CANDIDATE** | `perf_status=UNMEASURED`, P2 |
| `range_strategy_v1` | CANDIDATE | **Maintenir CANDIDATE** | Runtime-surfaces=none (doc-only), `perf_status=UNMEASURED` |
| `btc_coinm_accumulation` | CANDIDATE | **Maintenir CANDIDATE** | Doc-only concept, `perf_status=UNMEASURED` |
| `DCA_ON_FEAR_SOLID_STOCKS` | CANDIDATE | **Maintenir CANDIDATE** | Doc-only framework, `perf_status=UNMEASURED` |
| `e2e_dry_run` | FIXTURE | **Maintenir FIXTURE** | Fixture E2E uniquement, jamais de production |

## Règle de promotion

Aucune stratégie ne peut passer de `CANDIDATE` à `ACTIVE` tant que `perf_status=UNMEASURED`. Condition minimale : mesure via perf_engine ou backtest validé.

## Aucun retrait

Aucune stratégie ne satisfait les critères de retrait (retirement exige : stratégie remplacée, ou confirmée non-viable, ou conflictuelle avec une autre).

## Conclusion

Le registry est stable. Toutes les entrées restent `CANDIDATE` ou `FIXTURE`. Aucune modification du fichier `95_STRATEGY_REGISTRY.md` n'est requise à ce stade.
