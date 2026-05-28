---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_VARIANT_EDGE_ANALYSIS_01
status: DONE
verdict: PASS_XAU_SESSION_OPEN_VARIANT_EDGE_ANALYSIS_01
pr: TBD
merge_commit: TBD
---

Analyse edge par variant sur 33 jours Dukascopy (46 trades non-neutral). `xau_open_sweep_fvg` est le seul variant avec edge positif : 40% wr, avg_r +0.71 sur 20 trades. `xau_open_sweep_no_fvg` est le drag principal : 17% wr, avg_r -0.37 sur 23 trades. Commande `variant-report` et filtre variant (`--variants`) implémentés. 24 tests PASS.

## delivered

- `variant_report` command — breakdown W/L/T/wr/avg_r par variant depuis TRADES_JSONL
- Filtre variant dans `process_market_run`/`batch_run`/`run_with_outcomes` — arg positionnel 5 (csv,session,start,end,variants)
- `modules/trading_lab_v1/tests/test_variant_edge_analysis.py` — 11 tests (variant_report + filter)
- 24 tests PASS (11 nouveaux + 13 régression)

## result

| variant | n | W | L | T | wr | avg_r |
|---|---|---|---|---|---|---|
| xau_open_sweep_fvg | 20 | 8 | 6 | 6 | **40%** | **+0.71** |
| xau_open_sweep_no_fvg | 23 | 4 | 15 | 4 | 17% | -0.37 |
| xau_open_no_sweep_fvg | 1 | 0 | 1 | 0 | 0% | -1.0 |
| xau_open_no_sweep_no_fvg | 2 | 0 | 2 | 0 | 0% | -1.0 |

Break-even théorique à RR 2:1 = 33.3%. `sweep_fvg` dépasse ce seuil.

## remaining_gap

- Valider sweep_fvg sur dataset plus large (>30 trades) avant promotion perf_status sweep_fvg
- Investiguer les 6 timeouts sweep_fvg (21% timeout_rate — acceptable mais à surveiller)
- Prochaine étape : run-with-outcomes filtré `xau_open_sweep_fvg` sur dataset étendu
