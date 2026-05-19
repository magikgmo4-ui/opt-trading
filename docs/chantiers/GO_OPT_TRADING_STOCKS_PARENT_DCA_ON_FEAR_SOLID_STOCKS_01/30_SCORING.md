# Scoring — Fear Entry Signal

## Fear indicators

| Indicator | Weight | Fear threshold |
|---|---|---|
| VIX | 30% | > 25 (elevated), > 35 (high fear) |
| SPY drawdown from ATH | 25% | > -10% (correction), > -20% (bear) |
| CNN Fear & Greed | 15% | < 25 (extreme fear) |
| Put/Call ratio | 10% | > 1.2 |
| High yield spread | 10% | > 500 bps over Treasuries |
| 52-week low % (NYSE) | 10% | > 30% of stocks at 52wk low |

## Entry score

Score = sum(weight × indicator_binary) where indicator_binary = 1 if threshold met.

| Score | Zone | Action |
|---|---|---|
| >= 0.7 | Extreme fear | Full DCA allocation |
| 0.4 — 0.7 | Elevated fear | Half DCA allocation |
| < 0.4 | Normal | Accumulate cash, no DCA |

## Exit score (fundamentals only)

| Signal | Action |
|---|---|
| Revenue declining 3 consecutive quarters | Review position |
| Debt/EBITDA > 5x | Exit position |
| Dividend suspended | Exit position |
| Regulatory action / fraud investigation | Exit immediately |
