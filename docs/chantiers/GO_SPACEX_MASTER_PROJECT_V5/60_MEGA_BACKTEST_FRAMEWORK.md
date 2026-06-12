# Mega Backtest Framework

## First pass implemented

- `python3 -m modules.ipo_tracking.cli backtest-orb --csv <ohlcv.csv> --minutes 15`

## Required data

CSV columns:

```text
timestamp,open,high,low,close,volume
```

## Setups to add next

1. GAP_AND_GO
2. VWAP_RECLAIM
3. FVG_RECLAIM
4. IPO_PRICE_FLUSH_RECLAIM
5. FIRST_RED_DAY_TRAP
6. NEWS_CATALYST_BREAKOUT
7. MULTI_TF_CONTINUATION

## Metrics

- winrate
- expectancy R
- profit factor
- max drawdown
- average bars held
- best/worst regime
- leverage stress envelope
