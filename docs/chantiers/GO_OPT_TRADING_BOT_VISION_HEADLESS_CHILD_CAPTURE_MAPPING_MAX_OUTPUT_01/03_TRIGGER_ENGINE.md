---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01_TRIGGERS
doc_type: trigger_engine
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01
---

# 03_TRIGGER_ENGINE.md

Déclencheurs de capture : plan fixe et événementiel.

## 1_TRIGGERS_HORAIRES_FIXES

| Fenêtre (ET) | Pourquoi | Captures | Screen types |
|-------------|----------|----------|-------------|
| 04:00–05:00 | Pré-market Europe / commodities | DXY, gold, oil, BTC | DASHBOARD_MACRO |
| 08:00–09:30 | Pré-market US | Stocks, ETF, BTC, DXY | SCREENER_STOCKS, ETF_CRYPTO |
| 09:30 | Open US | BTC, ETF, stocks, DXY, gold | DASHBOARD_MACRO |
| 10:00–11:00 | Confirmation open | Charts + Coinglass | CHART_TECHNICAL + LIQUIDITY_* |
| 14:00 | Fenêtre Fed / macro | DXY, yields, gold, BTC | DASHBOARD_MACRO |
| 16:00 | Close US | ETF, stocks, BTC | ETF_CRYPTO, SCREENER_STOCKS |
| 20:00 | Futures / Asia prep | BTC, gold, oil | CHART_TECHNICAL |
| Funding windows | Perp pressure | Coinglass | FUNDING_COINGLASS, OI_COINGLASS |

## 2_TRIGGERS_PRIX_VOLATILITE

| Condition | Seuil | Capture |
|-----------|-------|---------|
| Price change 5m | >= 0.5% | CHART_TECHNICAL |
| Price change 15m | >= 1.0% | CHART_TECHNICAL |
| ATR spike | > 1.5x moyenne | CHART_TECHNICAL |
| Volume relatif | > 2.0x moyenne | CHART_TECHNICAL |
| Breakout HH/LL | Nouveau extremum | CHART_TECHNICAL |
| Cross EMA 20/50/200 | Cross | CHART_TECHNICAL |
| Supertrend flip | Flip | CHART_TECHNICAL |
| RSI | > 75 ou < 25 | CHART_TECHNICAL |
| MACD cross | Cross | CHART_TECHNICAL |
| VWAP reclaim/reject | Touch | CHART_TECHNICAL |

## 3_TRIGGERS_LIQUIDITE

| Condition | Seuil | Capture |
|-----------|-------|---------|
| OI change | > 10% en 1h | OI_COINGLASS |
| Funding rate | > 0.05% ou < -0.05% | FUNDING_COINGLASS |
| Liquidation cluster | Proche du prix spot | LIQUIDITY_COINGLASS |
| L/S ratio | > 2.0 ou < 0.5 | LS_RATIO_COINGLASS |
| Orderbook imbalance | Bid/ask > 3:1 | LIQUIDITY_COINGLASS |
| Large liquidation | > 10M USD | LIQUIDITY_COINGLASS |

## 4_TRIGGERS_MACRO

| Condition | Capture |
|-----------|---------|
| DXY breakout / breakdown | CHART_TECHNICAL (DXY) |
| US10Y spike > 10bp | CHART_TECHNICAL (US10Y) |
| Gold breakout (> 2% jour) | CHART_TECHNICAL (XAUUSD) |
| Oil breakout (> 3% jour) | CHART_TECHNICAL (BRENT) |
| VIX spike > 25 | CHART_TECHNICAL (VIX) |
| BTC diverge fortement du DXY ou gold | DASHBOARD_MACRO |

## 5_TRIGGERS_SCREENER

| Condition | Seuil | Capture |
|-----------|-------|---------|
| Stock volume relatif | > 2.0 | SCREENER_STOCKS |
| Stock move intraday | > 3% | SCREENER_STOCKS |
| Mega cap move | > 1.5% | SCREENER_STOCKS |
| Secteur cluster actif | 3+ stocks même secteur | SCREENER_STOCKS |
| Crypto stocks bougent avec BTC | 2+ stocks corrélés | SCREENER_STOCKS |

## 6_ARCHITECTURE_TRIGGER

```
Trigger engine (module séparé ou intégré à bot_vision_step2)
  ├── Scheduler (cron-like, fenêtres fixes)
  ├── Price watcher (WebSocket Binance ou polling)
  ├── Liquidity watcher (polling Coinglass)
  ├── Macro watcher (polling TV)
  └── Screener watcher (polling TV screener)
       ↓
  Décision : quel screen_type capturer ?
       ↓
  Appel : capture_headless.js --profile <dynamique> --once
       ↓
  Routage : screen_type → analyseur
```

Note : le trigger engine n'existe pas encore. Première version = scheduled only (timer bot_vision_step2 existant). Les triggers événementiels sont une P2.
