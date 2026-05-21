---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01_AUTOMATION_PLAN
doc_type: implementation_plan
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01
status: open
updated_at: 2026-05-20
---

# 10_BACKTEST_AUTOMATION_PLAN

## Architecture

```text
tools/strategy/daily_scalping/
  config.yaml          — paramètres variants, sessions, seuils
  load_data.py         — lecture CSV OHLCV, normalisation, fusion M5/M15
  indicators.py        — VWAP, ATR, session flags, ORB range
  detectors.py         — ORB, sweep, BOS/CHOCH proxy, retest
  scorer.py            — score /10 par setup
  simulator.py         — SL/TP, result_R, MFE, MAE, journal row
  report.py            — CSV journal + CSV résultats + markdown verdict
  run_backtest.py      — orchestrateur unique
```

## Pipeline détaillé

| Étape | Module | Entrée | Sortie |
|---|---|---|---|
| 1 | `load_data.py` | CSV M5 + CSV M15 | DataFrame OHLCV normalisé |
| 2 | `indicators.py` | DataFrame | +VWAP, +ATR, +session_flag, +orb_high, +orb_low |
| 3 | `detectors.py` | DataFrame enrichi | liste de setups candidats |
| 4 | `scorer.py` | setup candidat | setup + score /10 |
| 5 | `simulator.py` | setup scoré | journal row (result_R, MFE, MAE, …) |
| 6 | `report.py` | journal complet | CSV + markdown verdict |

## Variants

Chaque variant est un sous-ensemble des détecteurs activés :

| Variant | ORB | VWAP | Sweep/BOS | Score min |
|---|:---:|:---:|:---:|---:|
| `ORB_ONLY` | ✓ | — | — | 0 |
| `VWAP_PULLBACK_ONLY` | — | ✓ | — | 0 |
| `SMC_SWEEP_ONLY` | — | — | ✓ | 0 |
| `COMBINED_SMC_ORB_VWAP` | ✓ | ✓ | ✓ | 7 |

## Sorties attendues

```text
artifacts/backtests/daily_scalping/
  xauusd_m5_journal.csv          — 1 ligne par trade simulé
  xauusd_m5_results_by_variant.csv  — métriques agrégées par variant
  xauusd_m5_verdict.md           — verdict markdown auto-généré
```

## Phases d'implémentation

| Phase | Livrables | Tests |
|---|---|---|
| A | `load_data.py` + `indicators.py` | unittest DataFrame shape + colonnes |
| B | `detectors.py` | unittest setups détectés sur fixture |
| C | `scorer.py` | unittest scores sur setups connus |
| D | `simulator.py` | unittest result_R sur trades fixtures |
| E | `report.py` | unittest CSV + markdown valide |
| F | `run_backtest.py` | smoke end-to-end sur données synthétiques |
