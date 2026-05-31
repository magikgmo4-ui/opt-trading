---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01_CAPTURE_CONTRACT
doc_type: capture_contract
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01
---

# 20_CAPTURE_CONTRACT.md

Spécification de capture : viewport, fréquence, sections, full-page vs crop, multi-capture.

## 1_TYPES_DE_CAPTURE

| Type | Description | Viewport | Sections | Mode |
|------|-------------|----------|----------|------|
| `CHART_TECHNICAL_SCREEN` | Chart TradingView plein écran + indicateurs | 1920x1080 | Full page ou crop chart area | Full-page |
| `LIQUIDITY_DERIVATIVES_SCREEN` | Coinglass liquidation / funding / OI | 1920x1080 | Section heatmap + funding + OI + L/S | Multi-section |
| `MACRO_CROSS_ASSET_SCREEN` | Multi-chart BTC / Gold / DXY / Oil | 1920x1080 | Grille 2x2 | Full-page |
| `ETF_CRYPTO_SCREEN` | ETF BTC spot vs futures | 1920x1080 | Par ETF individuel | Single chart |
| `STOCK_SCREENER_SCREEN` | Screener actions | 1920x1080 | Tableau complet | Full-page |
| `NEWS_SENTIMENT_SCREEN` | News / calendar | 1920x1080 | Section news | Section |
| `COINGLASS_LIQUIDATION` | Liquidation heatmap | 1920x1080 | Full heatmap | Full-page |
| `COINGLASS_FUNDING` | Funding rate | 1920x1080 | Section funding | Section |
| `COINGLASS_OI` | Open interest | 1920x1080 | Section OI | Section |
| `COINGLASS_LS_RATIO` | Long/Short ratio | 1920x1080 | Section L/S | Section |

## 2_FORMAT_DE_CAPTURE

Chaque screenshot produit un fichier avec métadonnées embarquées :

```
data/screenshots/{capture_id}.png
```

Format minimal des métadonnées :

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
  "image_path": "data/screenshots/{capture_id}.png",
  "analysis_status": "pending|done|failed",
  "telegram_status": "none|sent|skipped",
  "deskpro_status": "pending|ingested"
}
```

## 3_VIEWPORT_ET_CROP

| Stratégie | Quand | Exemple |
|-----------|-------|---------|
| Full-page | Chart plein écran, screener, heatmap | CHART_TECHNICAL_SCREEN |
| Crop zone | Section spécifique d'une page | Funding rate panel uniquement |
| Multi-capture | Plusieurs sections d'une même page | Heatmap + Funding + OI + L/S en 4 screenshots |

## 4_FREQUENCE_DE_CAPTURE

### Plan fixe (time-based)

| Fenêtre | Captures | Justification |
|---------|----------|---------------|
| 04:00–05:00 ET | DXY, gold, oil, BTC | Pré-market Europe / commodities |
| 08:00–09:30 ET | Stocks, ETF, BTC, DXY | Pré-market US |
| 09:30 ET | BTC, ETF, stocks, DXY, gold | Open US |
| 10:00–11:00 ET | Charts + liquidity | Confirmation open |
| 14:00 ET | DXY, yields, gold, BTC | Fenêtre Fed / macro |
| 16:00 ET | ETF, stocks, BTC | Close US |
| 20:00 ET | BTC, gold, oil | Futures / Asia prep |
| Funding windows | Coinglass / exchange | Perp pressure |

### Triggers événementiels

Déclencher capture si :

**Prix / volatilité :**
- price_change_5m >= seuil
- price_change_15m >= seuil
- ATR_spike = true
- volume_relative > 2.0
- breakout previous high / low
- cross EMA 20/50/200
- supertrend flip
- RSI > 70 ou < 30
- MACD cross
- VWAP reclaim / rejection

**Liquidité :**
- open_interest_change élevé
- funding_rate extrême
- liquidation_cluster proche du prix
- long_short_ratio déséquilibré
- orderbook imbalance visible
- large liquidation event

**Macro :**
- DXY breakout / breakdown
- US10Y spike
- Gold breakout
- Oil breakout
- VIX spike
- BTC diverge fortement du DXY ou gold

**Screener :**
- stock relative volume > 2
- stock move > 3% intraday
- mega cap move > 1.5%
- sector cluster actif
- AI / defense / space trend détectée
- crypto stocks bougent avec BTC

## 5_TIME-FRAMES_CHART

| Timeframe | Usage | Priorité |
|-----------|-------|----------|
| 1m | Scalping / entrées fines | P1 |
| 5m | Intraday court | P1 |
| 15m | Intraday standard | P0 |
| 1h | Intraday moyen | P0 |
| 4h | Swing | P0 |
| 1D | Trend principal | P0 |

## 6_INDICATEURS_MINIMUM

| Indicateur | Rôle |
|------------|------|
| EMA 20 / 50 / 200 | Trend structure |
| VWAP | Fair value intraday |
| Volume | Confirmation |
| RSI | Momentum / extrêmes |
| MACD | Cross / divergence |
| Supertrend | Trend following stop |
| ATR | Volatilité |
| Bollinger Bands / Keltner | Volatility envelope |
| Volume Profile / VPVR | High-activity zones |

## 7_REPRODUCTIBILITE

- Même URL → même rendu (cache, time, thème fixe)
- Même viewport → mêmes proportions
- Même intervalle → mêmes données visibles
- Même thème TradingView (dark) → pas de variations cosmétiques
- Timeout capture : 30s max avant retry (max 3 retries)
