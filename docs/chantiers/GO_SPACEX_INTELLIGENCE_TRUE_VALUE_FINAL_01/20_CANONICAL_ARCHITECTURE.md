# 20_CANONICAL_ARCHITECTURE

## Parent

```text
GO_SPACEX_INTELLIGENCE_TRUE_VALUE_FINAL_01
```

## Superseded / absorbed

```text
GO_STOCK_TRUE_VALUE_ENGINE_01
GO_SPACEX_INTELLIGENCE_LAYER_01
GO_SPACEX_MASTER_PROJECT_V5
GO_SPACEX_FINAL_CANONICAL_01
```

`GO_SPACEX_FINAL_CANONICAL_01` remains the last full SpaceX implementation base. This bundle adds the true-value intelligence layer and consolidates governance.

---

## Canonical components

### 1. SpaceX Core

- SPCX quote/price/volume/VWAP.
- IPO price relation.
- opening range.
- gap vs IPO.
- relative volume.
- TradingView flags.
- SEC filings.
- news/catalysts.

### 2. SpaceX Intelligence

- Starlink.
- Starship.
- Falcon.
- NASA.
- FAA.
- FCC.
- DoD.
- index/ETF inclusion.
- xAI/Grok/GPU/datacenter signals.

### 3. Ecosystem Watchlist

- AI infra: NVDA, AVGO, AMD, MRVL, MU, PLTR, ARM.
- Semi: NVDA, AMD, AVGO, MU, MRVL, ARM, TSM.
- Space: SPCX, RKLB, LUNR, ASTS, RDW, PL, BKSY.
- Macro/reference: QQQ, NDX, SPY, BTCUSDT, XAUUSD.

### 4. True Value Layer

- fundamental_score.
- valuation_score.
- flow_score.
- surprise_score.
- hype_score.
- risk_score.
- confidence_score.

---

## Output principle

SpaceX-specific outputs may continue to exist:

```text
data/ipo/spacex/scored/latest_snapshot.json
data/data_center/views/spacex_super_desk/latest.json
outputs/spacex/scores/spacex_scores.json
```

The consolidated layer adds:

```text
outputs/spacex_true_value/latest/scores.json
outputs/spacex_true_value/latest/summary.md
outputs/stock_true_value/latest/scores.json
```

The final Data Center integration should choose one canonical latest view, not duplicate active producers.
