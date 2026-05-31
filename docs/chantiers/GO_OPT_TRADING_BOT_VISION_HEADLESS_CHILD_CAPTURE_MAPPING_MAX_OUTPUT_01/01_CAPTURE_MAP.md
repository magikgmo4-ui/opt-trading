---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01_CAPTURE_MAP
doc_type: capture_map
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01
---

# 01_CAPTURE_MAP.md

Mapping des actifs, sources et priorités de capture.

## A. Crypto majors

| Actif | Alias | Source | Priorité | TV Symbol | Timeframes |
|-------|-------|--------|----------|-----------|------------|
| BTCUSDT | BTC perp | TV + Coinglass | P0 | `BTCUSDT.P` | 15m, 1h, 4h, 1D |
| BTC spot | BTC index | TV | P0 | `BTCUSD` | 15m, 1h, 4h, 1D |
| ETHUSDT | ETH perp | TV + Coinglass | P1 | `ETHUSDT.P` | 15m, 1h, 4h |
| TOTAL | market cap | TV | P1 | `CRYPTOCAP:TOTAL` | 1D |
| TOTAL2 | ex-BTC cap | TV | P1 | `CRYPTOCAP:TOTAL2` | 1D |
| TOTAL3 | ex-ETH cap | TV | P1 | `CRYPTOCAP:TOTAL3` | 1D |
| BTC.D | dominance | TV | P1 | `CRYPTOCAP:BTC.D` | 1D |

## B. ETF crypto

| Actif | Source | Priorité | TV Symbol |
|-------|--------|----------|-----------|
| IBIT | TV stocks | P1 | `NASDAQ:IBIT` |
| FBTC | TV stocks | P1 | `NASDAQ:FBTC` |
| GBTC | TV stocks | P1 | `NYSE:GBTC` |
| BITB | TV stocks | P1 | `NYSE:BITB` |
| ARKB | TV stocks | P1 | `NASDAQ:ARKB` |

## C. Métaux / macro risk

| Actif | Alias | Source | Priorité | TV Symbol | Timeframes |
|-------|-------|--------|----------|-----------|------------|
| XAUUSDT | Gold crypto | TV exchange | P0 | `BITGET:XAUUSDT` | 15m, 1h, 4h |
| XAUUSD | Gold spot | TV forex | P0 | `OANDA:XAUUSD` | 15m, 1h, 4h, 1D |
| DXY | Dollar index | TV | P0 | `TVC:DXY` | 15m, 1h, 4h, 1D |
| US10Y | 10Y yield | TV | P1 | `TVC:US10Y` | 1D |
| VIX | Volatility | TV | P1 | `TVC:VIX` | 1D |

## D. Énergie

| Actif | Source | Priorité | TV Symbol | Timeframes |
|-------|--------|----------|-----------|------------|
| BZUSDT | Brent proxy | TV | P0 | `BITGET:BZUSDT` | 15m, 1h, 4h |
| BRENT | Brent oil | TV | P0 | `NYMEX:BC1!` | 1h, 4h, 1D |
| WTI | Crude oil | TV | P0 | `NYMEX:CL1!` | 1h, 4h, 1D |

## E. Coinglass derivatives

| Écran | URL Coinglass | Priorité |
|-------|---------------|----------|
| Liquidation heatmap | `coinglass.com/liquidation-data` | P0 |
| Funding rate | `coinglass.com/funding-rate` | P0 |
| Open interest | `coinglass.com/open-interest` | P0 |
| Long/Short ratio | `coinglass.com/long-short-ratio` | P0 |

## F. Stock screeners

| Screener | Filtre | Priorité |
|----------|--------|----------|
| Biggest caps | Market cap > 1T | P0 |
| AI / Tech | NVDA, AMD, PLTR, SMCI, AVGO, TSM, ARM | P1 |
| Defense | LMT, RTX, NOC, GD, HII, KTOS | P1 |
| Space | RKLB, LUNR, ASTS, PL, SPCE, IRDM | P2 |
| Crypto stocks | COIN, MSTR, MARA, RIOT, CLSK | P1 |
| Energy | XOM, CVX, OXY, SLB | P1 |

## G. Layouts de capture

| Layout | Actifs | Usage |
|--------|--------|-------|
| Single chart | 1 actif, 1 timeframe | Chart technique standard |
| Multi-chart 2x2 | 4 actifs, même TF | Dashboard macro (BTC, Gold, DXY, Oil) |
| Multi-chart 1x2 | 2 actifs, même TF | Comparaison paire |
| Table | N actifs | Screener / tableau de bord |

## H. Profils Playwright associés

| Profile | Contenu | Statut |
|---------|---------|--------|
| `profiles.btcusdt_poc.json` | BTCUSDT.P 15m single | ✅ Existant |
| `profiles.example.json` | BTCUSDT.P H1 single | ✅ Existant |
| À créer : multi-chart | BTC, Gold, DXY, Oil 2x2 | ❌ À faire |
| À créer : coinglass | Liquidation heatmap | ❌ À faire |
| À créer : screener | Biggest caps | ❌ À faire |
