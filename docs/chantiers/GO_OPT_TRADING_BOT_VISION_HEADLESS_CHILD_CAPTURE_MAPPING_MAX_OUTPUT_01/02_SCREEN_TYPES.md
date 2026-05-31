---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01_SCREEN_TYPES
doc_type: screen_types
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01
---

# 02_SCREEN_TYPES.md

Classification des types d'écran pour routage vers l'analyseur approprié.

## 1_TYPES_DE_SCREEN

| Type ID | Label | Source | Déclencheur | Analyseur |
|---------|-------|--------|-------------|-----------|
| `CHART_TECHNICAL` | Chart technique | TradingView | Horaire + prix | bot_vision_step2 (single) |
| `DASHBOARD_MACRO` | Dashboard macro 2x2 | TradingView | Horaire | bot_vision_step2 (quad) |
| `LIQUIDITY_COINGLASS` | Liquidations Coinglass | Coinglass | Horaire + liquidité | OCR spécialisé |
| `FUNDING_COINGLASS` | Funding rate | Coinglass | Horaire + funding extreme | OCR spécialisé |
| `OI_COINGLASS` | Open interest | Coinglass | Horaire + OI spike | OCR spécialisé |
| `LS_RATIO_COINGLASS` | Long/Short ratio | Coinglass | Horaire + déséquilibre | OCR spécialisé |
| `ETF_CRYPTO` | ETF BTC spot vs futures | TradingView | Horaire + BTC move | bot_vision_step2 (single) |
| `SCREENER_STOCKS` | Screener actions | TradingView | Horaire + screener trigger | Analyse texte |
| `NEWS_SENTIMENT` | News / calendar | TV / calendar | Événementiel | À définir |

## 2_SCHEMA_METADONNEES_CAPTURE

```json
{
  "capture_id": "uuid",
  "timestamp_utc": "2026-05-29T00:00:00Z",
  "source": "tradingview|coinglass|screener",
  "screen_type": "CHART_TECHNICAL",
  "asset": "BTCUSDT",
  "asset_class": "crypto",
  "timeframe": "15m",
  "url_key": "tradingview_btcusdt_15m",
  "indicators_visible": ["EMA20", "EMA50", "EMA200", "VWAP", "RSI", "MACD", "Volume"],
  "layout": "single|2x2|1x2|table",
  "trigger_type": "scheduled|price|volume|liquidity|macro|screener",
  "trigger_value": null,
  "image_path": "data/screenshots/{capture_id}.png",
  "image_size_bytes": null,
  "image_hash": "sha256:...",
  "analysis_status": "pending|done|failed",
  "telegram_status": "none|sent|skipped",
  "deskpro_status": "pending|ingested"
}
```

## 3_VIEWPORT_PAR_TYPE

| Screen type | Viewport | Full page | Sections |
|-------------|----------|-----------|----------|
| CHART_TECHNICAL | 1920x1080 | Oui | Chart area only |
| DASHBOARD_MACRO | 1920x1080 | Oui | 4 quadrants |
| LIQUIDITY_COINGLASS | 1920x1080 | Oui | Heatmap |
| FUNDING_COINGLASS | 1280x720 | Oui | Funding table |
| SCREENER_STOCKS | 1920x1080 | Oui | Full table |
| ETF_CRYPTO | 1920x1080 | Oui | Single chart |

## 4_CANAL_DE_TRAITEMENT

Chaque screen type est routé vers un analyseur existant ou à créer :

```
capture_headless.js (Playwright)
  → screen_type déterminé (par profile ou détection)
  → routage :
    ├── CHART_TECHNICAL → bot_vision_step2 (single mode)
    ├── DASHBOARD_MACRO → bot_vision_step2 (quad mode)
    ├── LIQUIDITY_*     → analyseur OCR Coinglass (à créer)
    ├── SCREENER_STOCKS → analyseur screener (à créer)
    └── ETF_CRYPTO      → bot_vision_step2 (single mode)
  → sortie :
    ├── data/deskpro/vision/runs/<id>/ (bot_vision_step2)
    ├── /opt/trading/desk/snapshots/ (desk_snapshot_ingest)
    └── vision_analysis.v1 (stub ou complet via adapter)
```
