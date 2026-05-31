# 01 — Target Assets

Assets sous surveillance bot_vision, classés par catégorie.

## Crypto majeures

| Symbole | Screen types | Timeframes | Priorité |
|---------|-------------|------------|----------|
| BTCUSDT.P | CHART_TECHNICAL, LIQUIDITY_COINGLASS, FUNDING_COINGLASS, OI_COINGLASS, LS_RATIO_COINGLASS | 15m, 1h, 4h, 1d | 1 (max) |
| ETHUSDT.P | CHART_TECHNICAL, LIQUIDITY_COINGLASS, FUNDING_COINGLASS, OI_COINGLASS, LS_RATIO_COINGLASS | 15m, 1h, 4h, 1d | 1 |

## Crypto market aggregates

| Symbole | Screen types | Timeframes |
|---------|-------------|------------|
| TOTAL | CHART_TECHNICAL | 1d, 1w |
| TOTAL2 | CHART_TECHNICAL | 1d, 1w |
| TOTAL3 | CHART_TECHNICAL | 1d, 1w |
| BTC.D | CHART_TECHNICAL | 1d, 1w |

## ETF crypto spot

| Symbole | Screen types | Timeframes | Priorité |
|---------|-------------|------------|----------|
| NASDAQ:IBIT | ETF_CRYPTO | 1h, 1d | 2 |
| NASDAQ:FBTC | ETF_CRYPTO | 1h, 1d | 3 |
| GBTC | ETF_CRYPTO | 1h, 1d | 4 |
| BITB | ETF_CRYPTO | 1h, 1d | 4 |
| ARKB | ETF_CRYPTO | 1h, 1d | 4 |

## Macro

| Symbole | Screen types | Timeframes | Priorité | Dashboard slot |
|---------|-------------|------------|----------|----------------|
| OANDA:XAUUSD | CHART_TECHNICAL, DASHBOARD_MACRO | 1h, 4h, 1d | 2 | top-right |
| TVC:DXY | CHART_TECHNICAL, DASHBOARD_MACRO | 1h, 4h, 1d | 2 | bottom-left |
| TVC:US10Y | CHART_TECHNICAL | 1h, 4h, 1d | 3 | — |
| TVC:VIX | CHART_TECHNICAL | 1h, 4h | 3 | — |
| FX:EURUSD | CHART_TECHNICAL | 1h, 4h | 3 | — |

## Commodities / énergie

| Symbole | Screen types | Timeframes | Priorité |
|---------|-------------|------------|----------|
| NYMEX:CL1! (WTI) | CHART_TECHNICAL | 1h, 4h, 1d | 2 |
| BZUSDT (Brent) | CHART_TECHNICAL | 1h, 4h, 1d | 3 |
| NYMEX:NG1! (Gaz) | CHART_TECHNICAL | 1h, 4h, 1d | 4 |
| Essence (RB1!) | CHART_TECHNICAL | 1h, 4h, 1d | 4 |

## Equity index

| Symbole | Screen types | Timeframes | Priorité | Dashboard slot |
|---------|-------------|------------|----------|----------------|
| SPY | CHART_TECHNICAL, DASHBOARD_MACRO | 1h, 4h, 1d | 2 | bottom-right |

## Screeners (TradingView / web)

Ces symboles sont des labels logiques — chaque screener correspond à une page web specific.

| Label logique | Categorie | Screen type | URL cible |
|--------------|-----------|-------------|-----------|
| SCREENER_BIGGEST_CAPS | screener | SCREENER_STOCKS | biggest caps page |
| SCREENER_TRENDING | screener | SCREENER_STOCKS | trending stocks |
| SCREENER_AI | screener | SCREENER_STOCKS | AI sector |
| SCREENER_DEFENSE | screener | SCREENER_STOCKS | defense sector |
| SCREENER_SPATIAL | screener | SCREENER_STOCKS | spatial sector |
| SCREENER_CRYPTO_STOCKS | screener | SCREENER_STOCKS | crypto-related stocks |
| SCREENER_ENERGY | screener | SCREENER_STOCKS | energy sector |

## Registre machine

Voir `modules/bot_vision/headless_capture/capture_map.json` pour la définition exploitable par code.
