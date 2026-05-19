# Backtest — DCA on Fear Framework

## Test periods

| Period | Event | Duration | SPY drawdown |
|---|---|---|---|
| 2008-2009 | Global Financial Crisis | 17 months | -56% |
| 2020 Q1 | COVID crash | 2 months | -33% |
| 2022 | Inflation / rate hikes | 10 months | -25% |
| 2011 Q3 | Debt ceiling / downgrade | 3 months | -19% |
| 2015 Q3 | China shock | 2 months | -12% |

## Metrics

| Metric | Target |
|---|---|
| CAGR vs SPY | > SPY + 2% |
| Max drawdown | < SPY drawdown |
| Sharpe ratio | > 1.0 |
| Win rate (positions) | > 60% |
| Average hold | > 12 months |

## Implementation plan

1. Build screener for solid stocks per classification rules
2. Implement fear scoring (daily data feed)
3. Simulate DCA entries on historical fear periods
4. Compare vs buy-and-hold SPY
5. Report: CAGR, max DD, Sharpe, win rate, exposure

## Next steps

- V1: manual paper trading on next fear event
- V2: automate data feed + scoring
- V3: live alert on fear entry signal
