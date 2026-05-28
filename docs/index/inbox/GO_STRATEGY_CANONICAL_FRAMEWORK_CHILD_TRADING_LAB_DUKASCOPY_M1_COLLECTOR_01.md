---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_DUKASCOPY_M1_COLLECTOR_01
status: DONE
verdict: PASS_TRADING_LAB_DUKASCOPY_M1_COLLECTOR_01
pr: 876
merge_commit: 74629ddf
---

Collecteur Dukascopy XAUUSD M1 opérationnel. Source HTTP publique accessible sans auth. 22 tests PASS. Smoke : 8640 candles (5 jours réels). Pipeline end-to-end sur données broker : 12 sessions → 1W/9L/2T avg_r=-0.7. perf_status reste UNMEASURED (5 jours ≪ seuil 30j). Prochaine étape : collecter 30–90 jours pour mesure décisionnelle.

## delivered

- `tools/trading_lab/collect_dukascopy_xauusd_m1.py` — collecteur bi5 LZMA → CSV
- `tools/trading_lab/tests/test_collect_dukascopy_m1.py` — 22 tests (URL, decode, TZ, OHLC, CSV, mock)
- Audit format bi5 documenté (champ order, price divisor 1000)

## result

- Source : HTTP 200, no auth, 1440 candles/day
- 87/87 tests PASS (full suite)
- Smoke 5j : 8640 candles → pipeline 1W/9L/2T avg_r=-0.7

## remaining_gap

- Collecter ≥ 30 jours pour atteindre seuil de décision perf_status
- Auditer sessions neutral (4/12 sur cette semaine volatile)
- GO_TRADING_LAB_REAL_BROKER_MEASUREMENT_02 avec CSV 30–90 jours
