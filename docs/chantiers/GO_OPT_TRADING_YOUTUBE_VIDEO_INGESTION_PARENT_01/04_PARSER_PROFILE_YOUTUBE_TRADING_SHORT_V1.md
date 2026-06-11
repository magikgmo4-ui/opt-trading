---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_PARSER_PROFILE_YOUTUBE_TRADING_SHORT_V1
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: parser_profile
status: draft_reference
created_at: 2026-06-06
parser_profile: youtube_trading_short_v1
---

# 04_PARSER_PROFILE_YOUTUBE_TRADING_SHORT_V1

## Objectif

Définir le parser initial pour vidéos courtes trading.

Le parser doit extraire des signaux candidats, pas générer des décisions de trading.

## Entrée

```json
{
  "video_id": "...",
  "title": "...",
  "description": "...",
  "spoken_transcript": "...",
  "screen_text": "...",
  "ocr_segments": []
}
```

## Sortie

```json
{
  "video_id": "...",
  "asset": "XAUUSD",
  "market_type": "forex|crypto|index|stock|unknown",
  "direction": "long|short|neutral|unknown",
  "entry": null,
  "stop_loss": null,
  "take_profits": [],
  "timeframe": null,
  "indicators": [],
  "pattern": null,
  "strategy_rules": [],
  "risk_rules": [],
  "confidence": 0.0,
  "missing_fields": [],
  "raw_evidence": []
}
```

## Détecteurs requis

### Asset detector

Alias :

```text
xau, gold, xauusd → XAUUSD
btc, bitcoin, btcusdt → BTCUSDT
eth, ethereum, ethusdt → ETHUSDT
nasdaq, nq, us100 → NASDAQ/US100
spx, s&p, us500 → SPX/US500
```

### Direction detector

Mots-clés :

```text
buy, long, bullish, pump, upside, breakout
sell, short, bearish, dump, downside, breakdown
```

### Entry detector

Patterns :

```text
entry 2345
buy above 2345
sell below 2345
zone 2340-2350
```

### SL/TP detector

Patterns :

```text
sl 2330
stop loss 2330
tp 2360
tp1 2360 tp2 2375 tp3 2390
target 2360
```

### Timeframe detector

```text
M1 M5 M15 M30 H1 H4 D1 W1
1m 5m 15m 1h 4h daily weekly
```

### Indicator detector

```text
EMA, SMA, RSI, MACD, VWAP, Bollinger, Fibonacci, liquidity, order block, FVG, support, resistance, trendline
```

## Confidence scoring

Base indicative :

```text
+0.25 asset détecté
+0.20 direction détectée
+0.20 entry détectée
+0.15 SL détecté
+0.10 TP détecté
+0.10 timeframe ou indicateur détecté
```

Seuils :

```text
>= 0.75 candidate_complete
0.50 - 0.74 candidate_partial
0.25 - 0.49 context_only
< 0.25 reject_noise
```

## Règles de prudence

- Ne jamais convertir un contenu éducatif en signal s'il n'y a pas d'entrée/direction explicite.
- Ne jamais inventer TP/SL.
- Si audio et OCR divergent, marquer `conflict_detected`.
- Prioriser les preuves OCR pour chiffres affichés.
