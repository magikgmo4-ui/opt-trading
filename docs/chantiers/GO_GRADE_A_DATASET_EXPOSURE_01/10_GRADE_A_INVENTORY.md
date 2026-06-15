# 10_GRADE_A_INVENTORY

## Dataset 1 — vision_analysis (25 symbols)

| Attribut | Valeur |
|----------|--------|
| Producteur | bot_vision/headless_capture + bot_vision_step2 (GPT-4.1-mini) |
| Fichiers | `data/data_center/views/vision_analysis/by_symbol/*.json` (25 fichiers, 25 MB) |
| Fraicheur | <1h, `freshness_state: "fresh"` |
| Qualite | GPT-4.1-mini analyzed, structured |
| Actifs | BTC, ETH, SOL, XRP, DOGE, XAUUSD, DXY, SPY, VIX, US10Y, WTI, NG, RB, IBIT, FBTC, ARKB, BITB, GBTC, TOTAL, TOTAL2, TOTAL3, BTC.D, EURUSD, BZUSDT |
| Expose via DeskPro | Oui (`/desk/vision`, `/desk/vision/news`, `/desk/vision/screener`) |
| Expose via /read/* | Non |
| Expose via Voice | Non (seul SPCX est expose) |
| Champs cles | price, trend, support, resistance, rsi, macd, volume, pattern, confidence, freshness_state |

## Dataset 2 — spacex_super_desk (SPCX)

| Attribut | Valeur |
|----------|--------|
| Producteur | ipo_tracking/collectors/ (12+ collectors) |
| Fichiers | `data/data_center/views/spacex_super_desk/latest.json` (180 KB) |
| Fraicheur | Pipeline (last write Jun 14, status=ok) |
| Qualite | Scored, enrichi |
| Actifs | SPCX |
| Expose via DeskPro | Oui (`/desk/spacex`, `/desk/spacex/snapshot`, `/desk/spacex/command-center`) |
| Expose via /read/* | Oui (`/read/spacex`) |
| Expose via Voice | Oui (spcx_full, spcx_risk, Resume SPCX) |
| Champs cles | price, gap_ipo, volume, VWAP, edge_score, open_score, action, confidence, top_setup, sector_regime, ipo_analogs, risks, entry/stop/tp1/tp2, market_state, sources_ok, pipeline_healthy, orderflow_score, ownership_pressure_score, vwap_state, vwap_score, source_quality |

## Dataset 3 — telegram_signals (scored)

| Attribut | Valeur |
|----------|--------|
| Producteur | telegram_screener (parser → normalizer → signal_producer) |
| Fichiers | `data/telegram_screener/signals/*.json` (300+ fichiers), `data/data_center/views/telegram_signals/` (212 MB history) |
| Fraicheur | Daily batch 05:30Z |
| Qualite | Scored, qualified, channel outcome tracked |
| Actifs | 115+ channels, BTC, XAU, EURUSD, GBPUSD, USDJPY, etc. |
| Expose via DeskPro | Oui (`/cms/signals`, `/desk/vision/telegram-claim`) |
| Expose via /read/* | Oui (`/read/alerts` — mais seulement 3 signaux) |
| Expose via Voice | Oui (`Alertes Telegram` → 3 alertes) |
| Champs cles | channel, pair, direction, entry, tp, sl, confidence, score, timestamp, qualification |

## Dataset 4 — deskpro analysis report

| Attribut | Valeur |
|----------|--------|
| Producteur | bot_vision_step2 → GPT-4.1-mini |
| Fichiers | `data/deskpro/inputs/analysis_report/latest.json` (43 KB) |
| Fraicheur | Vision pipeline (<1h) |
| Qualite | GPT analyzed, structured |
| Actifs | SPCX + multi-symbol context |
| Expose via DeskPro | Oui (interne) |
| Expose via /read/* | Non |
| Expose via Voice | Non |
| Champs cles | analysis_text, verdict, confidence, key_levels, risks, recommendations |

## Dataset 5 — voice_events

| Attribut | Valeur |
|----------|--------|
| Producteur | Voice Operator API calls |
| Fichiers | `data/logs/voice_events.jsonl` (295 B) |
| Fraicheur | Real-time |
| Qualite | Direct usage telemetry |
| Actifs | N/A (usage data) |
| Expose via DeskPro | Non |
| Expose via /read/* | Non |
| Expose via Voice | Oui (`/voice/analytics`) |
| Champs cles | command, intent, endpoint, latency_ms, ok, source, ts |
