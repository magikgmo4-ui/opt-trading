---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01_INPUT_INVENTORY
doc_type: input_surfaces_inventory
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01
---

# 10_INPUT_SURFACES_INVENTORY.md

Catalogue canonique des sources d'entrée pour le pipeline headless.

## A. Crypto majors

| Actif | Alias | Source principale | Priorité | Type de page | Vue |
|-------|-------|-------------------|----------|--------------|-----|
| `BTCUSDT` | BTC perp | TradingView + Coinglass | P0 | Chart + derivatives | TV chart + liquidation heatmap + funding |
| `BTC` spot | BTC index / BTCUSD | TradingView | P0 | Chart | TV chart spot |
| `ETHUSDT` | ETH perp | TradingView + Coinglass | P1 | Chart + derivatives | TV chart + liquidation |
| `TOTAL / TOTAL2 / TOTAL3` | market cap crypto | TradingView | P1 | Chart | TV chart market cap |
| `BTC.D` | dominance BTC | TradingView | P1 | Chart | TV chart dominance |

## B. ETF crypto

| Donnée | Source | Priorité | Type de page | Vue |
|--------|--------|----------|--------------|-----|
| BTC ETF flows | TradingView stocks | P1 | Stock chart | IBIT / FBTC / GBTC / BITB / ARKB |
| ETH ETF flows | TradingView stocks | P2 | Stock chart | ETHE / ETHA / FETH |

## C. Métaux / macro risk

| Actif | Alias | Source | Priorité | Type de page | Vue |
|-------|-------|--------|----------|--------------|-----|
| `XAUUSDT` | Gold crypto pair | TradingView / exchange | P0 | Chart | TV chart crypto gold pair |
| `XAUUSD` | Gold spot | TradingView | P0 | Chart | TV chart forex gold |
| `DXY` | Dollar index | TradingView | P0 | Chart | TV chart dollar index |
| `US10Y` | rendement 10 ans | TradingView | P1 | Chart | TV chart yield |
| `VIX` | stress marché | TradingView | P1 | Chart | TV chart volatility |

## D. Énergie

| Actif | Alias | Source | Priorité | Type de page | Vue |
|-------|-------|--------|----------|--------------|-----|
| `BZUSDT` | Brent proxy Bitget | TradingView / exchange | P0 | Chart | TV chart crypto oil pair |
| `BRENT` | Brent oil | TradingView | P0 | Chart | TV chart commodity |
| `WTI` | crude oil | TradingView | P0 | Chart | TV chart commodity |
| Gasoline / essence | RB futures / proxy | TV / exchange | P2 | Chart | TV chart |

## E. Coinglass / derivatives intelligence

| Écran | Objectif | Priorité |
|-------|----------|----------|
| Liquidation heatmap | Zones de liquidations actives | P0 |
| Funding rate | Extreme funding detection | P0 |
| Open interest | OI expansion / flush | P0 |
| Long/Short ratio | Crowding detection | P0 |
| Order book imbalance | Order flow pressure | P1 |
| Top trader ratio | Smart money proxy | P1 |
| Exchange liquidation clusters | Cluster map per exchange | P1 |

## F. Stocks screener

| Screener | Objectif | Priorité |
|----------|----------|----------|
| Biggest caps | Apple, Microsoft, Nvidia, Amazon, Meta, Google, Tesla | P0 |
| Trending stocks | Rotation sectorielle du jour | P1 |
| AI stocks | NVDA, AMD, PLTR, SMCI, AVGO, TSM, ARM | P1 |
| Defense stocks | LMT, RTX, NOC, GD, HII, KTOS | P1 |
| Space stocks | RKLB, LUNR, ASTS, PL, SPCE, IRDM | P2 |
| Crypto stocks | COIN, MSTR, MARA, RIOT, CLSK | P1 |
| Oil / energy stocks | XOM, CVX, OXY, SLB | P1 |

## G. Macro dashboard

| Vue | Objectif | Priorité |
|-----|----------|----------|
| Multi-chart 2x2 ou 3x2 | BTC / Gold / DXY / Oil corrélation | P0 |
| Economic calendar | Events à fort impact | P1 |
| Earnings calendar | Earnings reports | P2 |

## H. Format d'entrée requis par source

| Source | URL pattern | Auth needed | Viewport recommandé |
|--------|-------------|-------------|---------------------|
| TradingView chart | `https://www.tradingview.com/chart/?symbol=...` | Non (read-only) | 1920x1080 |
| Coinglass | `https://www.coinglass.com/...` | Non (read-only) | 1920x1080 |
| Screener TV | `https://www.tradingview.com/screener/...` | Non (read-only) | 1920x1080 |

## I. Priorisation générale

| Priorité | Critère | Délai |
|----------|---------|-------|
| P0 | Core trading (BTC, Gold, Oil, DXY) — impact direct sur décision | Immédiat |
| P1 | Support de décision (ETF, Coinglass, screener) | Court terme |
| P2 | Enrichissement (Space stocks, Gasoline, Earnings) | Moyen terme |
