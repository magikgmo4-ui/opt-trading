# 05 — Screen Types

## Registry

Fichier machine : `modules/bot_vision/headless_capture/screen_types.json`

## Types normalisés

### CHART_TECHNICAL
- Source : TradingView
- Layout : single
- Analyse : bot_vision_step2 (OpenAI Vision)
- Telegram : send_if_high_confidence
- Capture profile : profiles.production.json

### DASHBOARD_MACRO
- Source : TradingView (4 charts)
- Layout : quad (composé 2x2)
- Analyse : compose_quad.py → bot_vision_step2 (CROP_MODE=quad)
- Telegram : send_if_high_confidence
- Capture profile : profiles.macro_dashboard.json

### LIQUIDITY_COINGLASS / FUNDING_COINGLASS / OI_COINGLASS / LS_RATIO_COINGLASS
- Source : Coinglass
- Layout : single
- Analyse : stub (OCR analyzer A-07 TBD)
- Telegram : send_if_critical
- Capture profile : profiles.coinglass.json

### ETF_CRYPTO
- Source : TradingView
- Layout : single
- Analyse : bot_vision_step2
- Telegram : send_if_high_confidence
- Capture profile : profiles.production.json

### SCREENER_STOCKS
- Source : TradingView screener (7 pages)
- Layout : single
- Analyse : stub (screener analyzer A-08 TBD)
- Telegram : send_if_critical

### NEWS_SENTIMENT
- Source : News aggregators
- Layout : single
- Analyse : stub (sentiment analyzer A-09 TBD)
- Telegram : send_if_critical

## Politiques Telegram associées

| Politique | Condition | Comportement |
|-----------|-----------|-------------|
| send_if_high_confidence | ≥1 signal avec confidence ≥ 0.75 | Envoyer résumé filtré |
| send_if_critical | Événement seuil dépassé ($50M liq, etc.) | Envoyer alerte critique |

## Gaps

- Coinglass OCR analyzer (A-07) : non implémenté
- Screener analyzer (A-08) : non implémenté
- News sentiment analyzer (A-09) : non implémenté
