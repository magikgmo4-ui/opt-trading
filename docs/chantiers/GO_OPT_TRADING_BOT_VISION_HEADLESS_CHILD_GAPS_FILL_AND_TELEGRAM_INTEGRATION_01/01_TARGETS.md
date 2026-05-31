# 01 — Targets

## 1. Telegram effectif

**Avant** : `telegram_filter.py` sortait un JSON avec `{send: true, summary: "..."}` mais l'appel à Telegram n'était pas fait.

**Après** : `run_vision_pipeline.py` lit le JSON du filtre et appelle `shared/telegram_notify.send_telegram(summary)` si `send=true`.

Flags ajoutés :
- `--no-telegram` : skip l'envoi même si le filtre le demande
- `--telegram-threshold 0.70` : seuil de confiance personnalisé

## 2. Market hours

**Avant** : toutes les captures tournaient 24/7, y compris les ETF US la nuit et le weekend.

**Après** : `capture_headless.js` vérifie `isInMarketHours(symbol)` avant chaque capture.

Règles :
- USDT / BZUSDT / CRYPTOCAP:* → 24/7
- NASDAQ:* / NYSE:* / OTC:* / SPY / TVC:* / NYMEX:* → US market hours (Mon-Fri 09:30-16:00 ET)
- FX:* / OANDA:* → Forex (24h mais window 00:00-23:00 UTC)

Désactivable : `BOT_VISION_MARKET_HOURS=0`

## 3. Profils de capture manquants

14 nouveaux profils dans `profiles.supplementary.json` :

| Asset | Timeframes | Screen type |
|-------|-----------|-------------|
| CRYPTOCAP:TOTAL | 1d, 1w | CHART_TECHNICAL |
| CRYPTOCAP:TOTAL2 | 1d | CHART_TECHNICAL |
| CRYPTOCAP:TOTAL3 | 1d | CHART_TECHNICAL |
| CRYPTOCAP:BTC.D | 1d | CHART_TECHNICAL |
| NASDAQ:FBTC | 1h | ETF_CRYPTO |
| OTC:GBTC | 1h | ETF_CRYPTO |
| NASDAQ:BITB | 1h | ETF_CRYPTO |
| NASDAQ:ARKB | 1h | ETF_CRYPTO |
| BZUSDT (Brent) | 1h, 4h | CHART_TECHNICAL |
| NYMEX:CL1! (WTI) | 4h | CHART_TECHNICAL |
| NYMEX:NG1! (Gaz) | 4h | CHART_TECHNICAL |
| SCREENER_BIGGEST_CAPS | 1d | SCREENER_STOCKS |
