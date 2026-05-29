# 01_CAPTURE_MAP

## Univers de capture prioritaire

### A. Crypto majors

| Actif | Alias | Source principale | Priorite |
|---|---|---|---|
| `BTCUSDT` | BTC perp | TradingView + Coinglass | P0 |
| `BTC` spot | BTC index / BTCUSD | TradingView | P0 |
| `ETHUSDT` | ETH perp | TradingView + Coinglass | P1 |
| `TOTAL / TOTAL2 / TOTAL3` | market cap crypto | TradingView | P1 |
| `BTC.D` | dominance BTC | TradingView | P1 |

### B. ETF crypto

| Donnee | Source | Priorite |
|---|---|---|
| BTC ETF flows | source externe plus tard | P1 |
| IBIT / FBTC / GBTC | TradingView stocks / ETF | P1 |
| ETH ETF flows | plus tard | P2 |

### C. Metaux / macro risk

| Actif | Alias | Source | Priorite |
|---|---|---|---|
| `XAUUSDT` | Gold crypto pair | TradingView / exchange | P0 |
| `XAUUSD` | Gold spot | TradingView | P0 |
| `DXY` | Dollar index | TradingView | P0 |
| `US10Y` | rendement 10 ans | TradingView | P1 |
| `VIX` | stress marche | TradingView | P1 |

### D. Energie

| Actif | Alias | Source | Priorite |
|---|---|---|---|
| `BZUSDT` | Brent proxy Bitget | TradingView / exchange | P0 |
| `BRENT` | Brent oil | TradingView | P0 |
| `WTI` | crude oil | TradingView | P0 |
| Gasoline / essence | RB futures / proxy | P2 | |

### E. Stocks screener

| Screener | Objectif |
|---|---|
| Biggest caps | Apple, Microsoft, Nvidia, Amazon, Meta, Google, Tesla |
| Trending stocks | detecter la rotation du jour |
| AI | NVDA, AMD, PLTR, SMCI, AVGO, TSM, ARM |
| Defense | LMT, RTX, NOC, GD, HII, KTOS |
| Spatial | RKLB, LUNR, ASTS, PL, SPCE, IRDM |
| Crypto stocks | COIN, MSTR, MARA, RIOT, CLSK |
| Oil / energy | XOM, CVX, OXY, SLB |

## Mapping screenshots necessaires

| Screen family | Sources | Outputs cibles |
|---|---|---|
| `CHART_TECHNICAL_SCREEN` | TradingView charts | visual_context + vision_analysis + Data Center + DeskPro |
| `LIQUIDITY_DERIVATIVES_SCREEN` | Coinglass / exchange derivatives | vision_context source-specific + Telegram + DeskPro |
| `MACRO_CROSS_ASSET_SCREEN` | TradingView multi-chart macro | vision_analysis + Data Center + DeskPro |
| `ETF_CRYPTO_SCREEN` | TradingView ETF / stocks | vision_analysis + DeskPro |
| `STOCK_SCREENER_SCREEN` | TradingView screener / equivalent | watchlist payload + Data Center + Telegram filter |
| `NEWS_SENTIMENT_SCREEN` | news panels / calendars | summary payload + Telegram + DeskPro |

## Format minimal d'une capture

```json
{
  "capture_id": "uuid",
  "timestamp_utc": "2026-05-29T00:00:00Z",
  "source": "tradingview|coinglass|screener|calendar",
  "screen_type": "CHART_TECHNICAL_SCREEN",
  "asset": "BTCUSDT",
  "asset_class": "crypto",
  "timeframe": "15m",
  "url_key": "tradingview_btcusdt_15m",
  "indicators_visible": ["EMA20", "EMA50", "EMA200", "VWAP", "RSI", "MACD", "Volume"],
  "image_path": "data/screenshots/...",
  "analysis_status": "pending|done|failed",
  "telegram_status": "none|sent|skipped",
  "deskpro_status": "pending|ingested"
}
```
