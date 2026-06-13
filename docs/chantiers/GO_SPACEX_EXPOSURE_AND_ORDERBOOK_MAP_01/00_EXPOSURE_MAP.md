---
doc_id: GO_SPACEX_EXPOSURE_AND_ORDERBOOK_MAP_01
doc_type: documentary_architecture
go_id: GO_SPACEX_EXPOSURE_AND_ORDERBOOK_MAP_01
status: documented
created_at: 2026-06-12
---

# SPCX Exposure & Order Book Map

## Already Built (7 collectors)

| Collector | Scope | File |
|-----------|-------|------|
| Yahoo public | SPCX price, OHLCV, bars | `yahoo_public.py` |
| SEC EDGAR | Filings, prospectus, lockup | `sec_edgar.py` |
| RSS News | 40 headlines via Google News | `rss_news.py` |
| TradingView webhook | TV alerts → /tv/spacex | `tradingview_webhook.py` |
| Bot Vision adapter | DOM extraction, screenshots | `bot_vision_adapter.py` |
| Nasdaq quote | API quote, veto | `nasdaq_quote.py` |
| Desk/Sheets/Telegram | Context, exports | `desk_pro.py`, `sheets.py`, `telegram_signal.py` |

## New (SPCX V2 collectors)

| Collector | Scope | File |
|-----------|-------|------|
| News sentiment | Dedup, polarity, catalyst decay, sector halo | `spcx_news_sentiment.py` |
| Spot microstructure | Bid/ask/spread/liquidity from DOM | `spcx_microstructure.py` |
| Crypto risk proxy | BTC/ETH funding, OI, L/S ratio (max weight 0.05) | `binance_derivatives.py` |

## Architecture — 7 Levels

```
LEVEL 1 — SPCX DIRECT SPOT (P0)
  price, volume, bid/ask, L2 depth, tape, VWAP, auctions
  ✅ price, volume, bars (Yahoo)
  ✅ bid/ask/spread via DOM (spcx_microstructure)
  ⏳ L2 depth, tape, auctions (need broker/Nasdaq feed)

LEVEL 2 — SPCX OPTIONS (P1)
  chain, IV, put/call ratio, skew, gamma
  ❌ availability check only for now

LEVEL 3 — SPCX SHORT/BORROW (P1)
  short interest, borrow fee, utilization, FTD
  ❌ availability check only for now

LEVEL 4 — SPCX DERIVATIVES DIRECT (P1)
  futures, perp, CFD, tokenized stock
  ❌ availability check only for now

LEVEL 5 — ETF/FUND EXPOSURE (P2)
  ARKX, UFO, QQQ, Alphabet stake
  ✅ comparable DOM captures exist (ARKX, QQQ)
  ⏳ fund holding data not yet collected

LEVEL 6 — SECTOR HALO (P2)
  RKLB, ASTS, LUNR, PL, RDW, TSLA
  ✅ 7 symbols captured via Bot Vision MAX
  ✅ sector halo from DOM (spcx_news_sentiment)

LEVEL 7 — RISK PROXIES (P2, max weight 0.05)
  BTC/ETH derivatives, VIX, DXY, NQ/ES
  ✅ crypto funding/OI/LS (binance_derivatives)
  ⏳ VIX/DXY/NQ not yet wired
```

## Files to create next

```
modules/ipo_tracking/collectors/spcx_spot_orderbook.py     ← P0
modules/ipo_tracking/collectors/spcx_options_availability.py ← P1
modules/ipo_tracking/collectors/spcx_short_borrow.py       ← P1
modules/ipo_tracking/collectors/spcx_derivatives_availability.py ← P1
modules/ipo_tracking/collectors/spcx_fund_etf_exposure.py  ← P2
modules/ipo_tracking/collectors/spcx_sector_halo.py        ← P2
```
