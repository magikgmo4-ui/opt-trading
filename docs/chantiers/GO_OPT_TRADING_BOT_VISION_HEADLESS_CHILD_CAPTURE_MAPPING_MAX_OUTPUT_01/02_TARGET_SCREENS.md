# 02 — Target Screens

Définition des écrans attendus par screen type.

## CHART_TECHNICAL_SCREEN

| Champ | Valeur |
|-------|--------|
| Source | TradingView |
| Assets | BTCUSDT.P, ETHUSDT.P, TOTAL, TOTAL2, TOTAL3, BTC.D, OANDA:XAUUSD, TVC:DXY, TVC:US10Y, TVC:VIX, NYMEX:CL1!, BZUSDT, NYMEX:NG1!, SPY, FX:EURUSD |
| Timeframes | 15m, 1h, 4h, 1d, 1w selon priorité |
| Layout | Single chart |
| Indicateurs | EMA20, EMA50, EMA200, VWAP, RSI, MACD, Volume (variable par asset) |
| Capture frequency | 15m pour BTC/ETH, 1h pour macro, 4h pour commodities |
| Analyse | bot_vision_step2 → OpenAI Vision |
| Output JSON | vision_analysis.v1 |
| Telegram policy | send_if_high_confidence |

## LIQUIDITY_DERIVATIVES_SCREEN (Coinglass)

| Champ | Valeur |
|-------|--------|
| Source | Coinglass |
| Types | LIQUIDITY_COINGLASS, FUNDING_COINGLASS, OI_COINGLASS, LS_RATIO_COINGLASS |
| Assets | BTCUSDT.P, ETHUSDT.P |
| Layout | Single (full page browser capture) |
| Capture frequency | Every 4h |
| Analyse | OCR analyzer TBD (A-07) — stub pour l'instant |
| Telegram policy | send_if_critical (>=$50M liquidations) |

## MACRO_CROSS_ASSET_SCREEN (Dashboard)

| Champ | Valeur |
|-------|--------|
| Source | TradingView (4 charts composés) |
| Dashboard ID | macro_dashboard_01 |
| Slots | top-left (BTC), top-right (XAU), bottom-left (DXY), bottom-right (SPY) |
| Timeframe | 1h |
| Layout | Quad 2x2 → composé par compose_quad.py |
| Capture frequency | Every 4h |
| Analyse | compose_quad → bot_vision_step2 (CROP_MODE=quad) |
| Telegram policy | send_if_high_confidence |

## ETF_CRYPTO_SCREEN

| Champ | Valeur |
|-------|--------|
| Source | TradingView |
| Assets | NASDAQ:IBIT, NASDAQ:FBTC, GBTC, BITB, ARKB |
| Timeframes | 1h, 1d |
| Layout | Single |
| Capture frequency | Every 4h (market hours NY: 09:30-16:00 ET) |
| Analyse | bot_vision_step2 |
| Telegram policy | send_if_high_confidence |

## STOCK_SCREENER_SCREEN

| Champ | Valeur |
|-------|--------|
| Source | TradingView screener (7 pages) |
| Layout | Single (full page browser capture) |
| Capture frequency | Daily (08:00 UTC) |
| Analyse | Screener analyzer TBD (A-08) — stub |
| Telegram policy | send_if_critical |

## NEWS_SENTIMENT_SCREEN

| Champ | Valeur |
|-------|--------|
| Source | News aggregators (CoinDesk, CoinTelegraph, TheBlock) |
| Layout | Single |
| Capture frequency | Every 6h |
| Analyse | Sentiment analyzer TBD (A-09) — stub |
| Telegram policy | send_if_critical |
