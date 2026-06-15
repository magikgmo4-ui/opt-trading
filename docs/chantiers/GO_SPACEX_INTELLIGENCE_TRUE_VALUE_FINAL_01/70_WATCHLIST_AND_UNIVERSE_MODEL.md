# 70_WATCHLIST_AND_UNIVERSE_MODEL

## Universes

```yaml
CORE_WATCHLIST_PRIORITY:
  - SPCX
  - NVDA
  - AVGO
  - MU
  - AMD
  - MRVL
  - PLTR
  - ARM
  - TSM
  - RKLB
  - ASTS
  - LUNR

CORE_AI:
  - NVDA
  - AMD
  - AVGO
  - PLTR
  - ARM

CORE_SEMI:
  - NVDA
  - AMD
  - AVGO
  - MU
  - MRVL
  - ARM
  - TSM

CORE_SPACE:
  - SPCX
  - RKLB
  - LUNR
  - ASTS
  - RDW
  - PL
  - BKSY

CORE_MACRO:
  - QQQ
  - NDX
  - SPY
  - BTCUSDT
  - XAUUSD
```

## SPCX special-case rule

SPCX remains special-case until official live market data confirms listing status, tradability and available ratios.

If ratios are unavailable:

```yaml
disabled_metrics:
  - pe_forward
  - price_to_fcf
  - peg_ratio

additional_metrics:
  - backlog_score
  - launch_cadence_score
  - contract_pipeline_score
  - starlink_growth_proxy
  - index_flow_probability
```

## Invariant

Never infer official tradability from scenario text alone. Use live market data / official exchange source before marking `ESTABLISHED`.
