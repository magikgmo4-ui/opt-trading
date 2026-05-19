# Entry Model — DCA Rules

## Allocation

| Fear zone | Allocation per event | Max per stock | Max total |
|---|---|---|---|
| Extreme (score >= 0.7) | 2% of capital | 10% | 40% |
| Elevated (score 0.4-0.7) | 1% of capital | 5% | 20% |
| Normal (score < 0.4) | 0% | — | — |

## DCA cadence

| Condition | Frequency |
|---|---|
| Fear score >= 0.7 | Every 5 trading days while fear persists |
| Fear score 0.4-0.7 | Every 10 trading days |
| Fear score drops 0.2+ in 5 days | Accelerate: next day |

## Stock selection

1. Rank all solid stocks by drawdown from 52-week high (deepest first)
2. Pick top 5 by score (fundamentals + drawdown)
3. Equal weight allocation among selected

## Execution

- All orders limit (not market)
- Slippage budget: 0.1% per order
- No short selling, no margin
