---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_REAL_BROKER_MEASUREMENT_02
status: DONE
verdict: PASS_TRADING_LAB_REAL_BROKER_MEASUREMENT_02
pr: TBD
merge_commit: TBD
---

Mesure réelle sur 33 jours Dukascopy XAUUSD M1 (2026-03-10 → 2026-04-11). Filtre neutral implémenté : sessions direction=neutral skippées (aucun trade placé). Pipeline 46 trades réels : 12W/24L/10T, avg_r=0.0 (break-even). perf_status promu à MEASURED. Win rate 26% insuffisant pour edge positif — piste d'amélioration identifiée.

## delivered

- Filtre `first5_direction != "neutral"` dans `process_market_run` — sessions neutral → event+features écrits, aucun trade
- 13 tests d'intégration PASS (no regression)
- Mesure décisionnelle sur données broker réelles : critères remplis (≥20 trades, ≥30j, timeout 21.7% <30%)

## result

- 68 sessions observées sur 33 jours (25 bullish / 21 bearish / 22 neutral)
- 46 trades placés (22 neutral filtrés)
- 12W / 24L / 10T, avg_r=0.0
- Timeout rate 21.7% (sous seuil 30%)
- perf_status : MEASURED — pas d'edge positif à ce stade

## remaining_gap

- Win rate 26% < 34% seuil break-even théorique à RR 2:1
- Piste : analyser variant xau_open_sweep_fvg vs autres pour isoler edge
- Piste : investiguer les 24 pertes (direction assignment, SL placement)
