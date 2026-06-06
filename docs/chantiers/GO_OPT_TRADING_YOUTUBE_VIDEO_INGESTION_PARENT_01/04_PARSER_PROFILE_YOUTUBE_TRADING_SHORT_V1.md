---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_PARSER_PROFILE_YOUTUBE_TRADING_SHORT_V1
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: parser_profile
status: reference
created_at: 2026-06-06
surface: youtube_video_ingestion
parser_profile: youtube_trading_short_v1
---

# 04_PARSER_PROFILE_YOUTUBE_TRADING_SHORT_V1

## Objectif

Définir le premier parser pour vidéos trading courtes YouTube.

Le parser doit transformer transcript + OCR + metadata en données structurées, sans inventer les champs absents.

## Entrées

```json
{
  "title": "string",
  "description": "string|null",
  "spoken_transcript": "string|null",
  "screen_text": "string|null",
  "metadata": {}
}
```

## Sortie canonique

```json
{
  "video_id": "string",
  "parser_profile": "youtube_trading_short_v1",
  "assets": [],
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

## Détection actifs

Symboles prioritaires :

```text
XAUUSD, GOLD, BTC, BTCUSDT, ETH, ETHUSDT, NASDAQ, NQ, US30, DXY, EURUSD, GBPUSD, USDJPY
```

Normalisation :

```text
GOLD -> XAUUSD
XAU -> XAUUSD
BITCOIN -> BTCUSDT si contexte crypto
NASDAQ -> NASDAQ/NQ selon contexte
```

## Détection direction

```text
long: buy, long, bullish, call, upside, breakout up
short: sell, short, bearish, put, downside, breakdown
neutral: wait, no trade, range, avoid
unknown: ambigu ou absent
```

## Détection prix

Priorité :

```text
entry / buy at / sell at / zone / above / below
sl / stop / stop loss / invalidation
tp / target / take profit / partials
```

Règle : ne pas convertir une zone vague en entrée unique sans preuve.

## Timeframes

Détecter :

```text
M1, M3, M5, M15, M30, H1, H4, D1, W1
1m, 5m, 15m, 1h, 4h, daily, weekly
```

## Indicateurs

Détecter :

```text
EMA, SMA, RSI, MACD, VWAP, Fibonacci, volume, order block, FVG, liquidity, support, resistance, trendline, break of structure, BOS, CHoCH
```

## Stratégie

Extraire seulement les règles formulées ou visibles :

```text
condition d'entrée
condition d'invalidation
condition de prise de profit
filtre de tendance
filtre de liquidité
confirmation attendue
```

## Confidence score

Barème proposé :

```text
0.90+ actif + direction + entry + SL + TP prouvés
0.70  actif + direction + au moins une règle exploitable
0.50  actif ou thème clair, mais setup incomplet
0.30  contenu trading général sans signal structuré
0.00  non exploitable
```

## Raw evidence

Chaque extraction doit pointer vers une preuve :

```json
{
  "field": "direction",
  "value": "long",
  "source": "screen_text",
  "evidence": "BUY XAUUSD",
  "timestamp": "00:04"
}
```

## Modèle hybride

Ordre recommandé :

```text
regex déterministe
→ dictionnaires symboles/indicateurs
→ heuristiques trading
→ LLM contrôlé pour règles textuelles
→ validation JSON schema
```

## Invariants

- Ne pas inventer entry / SL / TP.
- Ne pas prendre un exemple éducatif pour un signal réel sans preuve.
- Ne pas classer une vidéo comme tradable si le signal est incomplet.
- Toujours conserver `missing_fields`.

## Sortie non tradable

```json
{
  "direction": "unknown",
  "entry": null,
  "stop_loss": null,
  "take_profits": [],
  "confidence": 0.3,
  "missing_fields": ["entry", "stop_loss", "take_profits"]
}
```