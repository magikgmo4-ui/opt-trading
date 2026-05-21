# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01

**État:** En cours
**Branche:** `go/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01`
**Parent:** `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`

Runner backtest automatisé `SMC_ORB_VWAP_SCALP_A_PLUS` — OHLCV → détection →
scoring → simulation → journal CSV → verdict markdown. 4 variants, XAUUSD M5/M15.

## Docs chantier

- `00_INITIAL_PROJECT_DOC.md` — Cadrage + pipeline cible
- `10_BACKTEST_AUTOMATION_PLAN.md` — Architecture + phases
- `20_DATA_CONTRACT.md` — Format CSV entrée/sortie
- `30_DETECTOR_RULES.md` — Règles mécaniques ORB/sweep/BOS/VWAP
- `40_REPORTING_CONTRACT.md` — Métriques + critères promotion auto

## Squelette code

```text
tools/strategy/daily_scalping/
  config.yaml, load_data.py, indicators.py, detectors.py,
  scorer.py, simulator.py, report.py, run_backtest.py
```

## Commande cible

```bash
python tools/strategy/daily_scalping/run_backtest.py \
  --symbol XAUUSD --timeframe M5 --context-timeframe M15 \
  --input data/market/xauusd_m5.csv \
  --context-input data/market/xauusd_m15.csv \
  --out artifacts/backtests/daily_scalping
```
