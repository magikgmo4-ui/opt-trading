# 10_METRICS_SPEC

## Métriques

| Métrique | Formule | Source |
|---|---|---|
| PnL total | Σ(exit_price - entry_price) × size | Tracked events |
| Win rate | winning_trades / total_trades | Tracked events |
| Sharpe ratio | (mean_return - rf) / σ(returns) | Returns series |
| Max drawdown | max(peak - trough) / peak | Equity curve |
| Profit factor | gross_profit / gross_loss | Tracked events |

## Module structure

```text
modules/perf_engine/
  metrics/
    __init__.py
    pnl_calculator.py
    sharpe_calculator.py
    drawdown_calculator.py
    win_rate_calculator.py
    metrics_aggregator.py
  tests/
    test_pnl.py
    test_sharpe.py
    test_drawdown.py
    test_win_rate.py
    test_aggregator.py
```
