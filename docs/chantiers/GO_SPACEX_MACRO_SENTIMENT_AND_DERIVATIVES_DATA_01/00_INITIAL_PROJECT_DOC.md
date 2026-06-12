---
doc_id: GO_SPACEX_MACRO_SENTIMENT_AND_DERIVATIVES_DATA_01_INITIAL
doc_type: initial_project_doc
go_id: GO_SPACEX_MACRO_SENTIMENT_AND_DERIVATIVES_DATA_01
status: draft
created_at: 2026-06-12
---

# GO_SPACEX_MACRO_SENTIMENT_AND_DERIVATIVES_DATA_01

## Phase 1 — News/Sentiment/Analysts/Macro

### Already collected (day-1)
- 40 headlines via Google News RSS
- 40 SEC filings (424B4 IPO prospectus)
- news_score: 1.0, catalyst: 1.0, info_trust: 1.0

### To build
- News dedup (same story × multiple sources → 1 cluster)
- Sentiment polarity (bullish/bearish/neutral per headline)
- Analyst score (coverage, consensus, price targets)
- Sector halo score (RKLB/ASTS/TSLA/QQQ from existing DOM captures)
- Catalyst decay (fresh < 2h → 1.0, >24h → 0.2)

## Phase 2 — Order Book / Derivatives

### Binance derivatives proxy
- `collectors/binance_derivatives.py` — BTC/ETH/SOL funding, OI, L/S ratio
- Scoring: funding_pressure, oi_pressure, crowding_risk, overall_risk

### To build next
- SPCX bid/ask/spread from Yahoo DOM
- Coinglass liquidations integration
- Futures order book depth

## Files
```
modules/spcx_v2/collectors/binance_derivatives.py — derivatives proxy collector + scoring
modules/ipo_tracking/collectors/rss_news.py — already fixed with Google News
```
