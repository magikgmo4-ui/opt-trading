# 02_SCREEN_TYPES

## `CHART_TECHNICAL_SCREEN`

Objectif : lecture technique pure.

Timeframes cibles : `1m`, `5m`, `15m`, `1h`, `4h`, `1D`

Indicateurs minimum :

- EMA 20 / 50 / 200
- VWAP
- Volume
- RSI
- MACD
- Supertrend
- ATR
- Bollinger Bands ou Keltner
- VPVR si disponible

Analyse attendue :

- `trend_direction`
- `market_structure`
- `support_resistance`
- `breakout_breakdown`
- `volatility_state`
- `momentum_state`
- `volume_confirmation`
- `invalidations`

## `LIQUIDITY_DERIVATIVES_SCREEN`

Objectif : comprendre la pression levier / liquidation.

Captures visees :

- liquidation heatmap
- funding rate
- open interest
- long/short ratio
- order book imbalance
- top trader ratio
- exchange liquidation clusters

Analyse attendue :

- `liquidity_zones`
- `long_squeeze_risk`
- `short_squeeze_risk`
- `funding_extreme`
- `oi_expansion_or_flush`
- `crowding_direction`
- `trap_probability`

## `MACRO_CROSS_ASSET_SCREEN`

Objectif : relier BTC / gold / oil / DXY / yields.

Layouts recommandes : `2x2` ou `3x2`, meme timeframe, meme plage temporelle.

Analyse attendue :

- `risk_on_risk_off`
- `dxy_pressure`
- `gold_safe_haven_bid`
- `oil_inflation_pressure`
- `btc_correlation_break`
- `macro_divergence`

## `ETF_CRYPTO_SCREEN`

Objectif : capter le narratif institutionnel BTC.

Analyse attendue :

- `etf_relative_strength`
- `btc_spot_confirmation`
- `gbtc_pressure`
- `institutional_bid_proxy`
- `gap_vs_spot`

## `STOCK_SCREENER_SCREEN`

Colonnes necessaires :

- `ticker`
- `price`
- `% change`
- `volume`
- `relative volume`
- `market cap`
- `sector`
- `pre-market / after-hours` si disponible
- `technical rating` si disponible
- `analyst rating` si disponible

Analyse attendue :

- `sector_rotation`
- `momentum_clusters`
- `risk_appetite`
- `theme_strength`
- `relative_volume_spike`
- `watchlist_candidates`

## `NEWS_SENTIMENT_SCREEN`

Sources possibles : TradingView news panel, Coinglass news, stock screener news,
crypto calendar, economic calendar, earnings calendar.

Analyse attendue :

- `event_type`
- `asset_impacted`
- `sentiment`
- `urgency`
- `price_reaction`
- `confirmed_or_unconfirmed`
