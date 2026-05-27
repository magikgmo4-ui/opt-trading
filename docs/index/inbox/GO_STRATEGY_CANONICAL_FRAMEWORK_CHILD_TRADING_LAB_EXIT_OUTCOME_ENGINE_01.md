---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_EXIT_OUTCOME_ENGINE_01
status: DONE
verdict: PASS_TRADING_LAB_EXIT_OUTCOME_ENGINE_01
pr: 868
merge_commit: 10ce8885153cc3e7e388c76b5f502cd060b831e6
---

Moteur de résolution d'issue déterministe pour trading_lab_v1. Scan post-entrée TP/SL avec règle conservative (même chandelier → loss). 25 tests PASS. Intégration : 6W/4L/0T avg_r=0.8 sur 10 sessions du CSV de référence. Champ `entry_candle_ts` ajouté aux features/trades.

## delivered

- `exit_outcome_v1.py` — calc_tp, resolve_exit_outcome, get_post_entry_candles
- `apply-outcomes` CLI dans trading_lab_v1.py
- `entry_candle_ts` ajouté aux features/trades
- `batch_report` enrichi : win_count, loss_count, timeout_count, avg_r_realized
- `sample_xauusd_m1_real_like.csv` étendu à 92 rows (post-entrée ciblés)

## result

- 25 tests PASS
- intégration 6W / 4L / 0T
- avg_r_realized = 0.8

## remaining_gap

- connecter apply_outcomes au pipeline complet
- mesurer sur données broker réelles depuis state/trading_lab_v1/inputs/
