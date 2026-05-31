---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01_DATA_CENTER
doc_type: data_center_handoff
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01
---

# 50_DATA_CENTER_HANDOFF.md

Schéma "max data out" vers Data Center.

## 1_PRINCIPES

- Data Center reçoit le maximum de données structurées
- Pas de filtage côté émission (c'est au consommateur de filtrer)
- Distinguer 4 catégories : raw_capture / extracted_signal / generated_summary / distribution_payload
- Chaque payload est autonome (capture_id + timestamp + source)

## 2_CATEGORIES_DE_PAYLOAD

| Catégorie | Contenu | Volumétrie |
|-----------|---------|------------|
| `raw_capture` | Métadonnées de capture (sans image), statut analyse | 1 par capture |
| `extracted_signal` | Signaux extraits par analyseur | 1 par analyse |
| `generated_summary` | Résumé texte + setup + niveaux | 1 par analyse significative |
| `distribution_payload` | Payload complet pour DeskPro/Telegram | 1 par payload distribué |

## 3_SCHEMA_MAX_DATA_OUT

```json
{
  "payload_id": "uuid",
  "payload_type": "raw_capture|extracted_signal|generated_summary|distribution_payload",
  "pipeline_version": "v1",
  "go_id": "GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01",

  "capture": {
    "capture_id": "uuid",
    "timestamp_utc": "2026-05-29T00:00:00Z",
    "source": "tradingview",
    "screen_type": "CHART_TECHNICAL_SCREEN",
    "asset": "BTCUSDT",
    "asset_class": "crypto",
    "timeframe": "15m",
    "url_key": "tradingview_btcusdt_15m",
    "indicators_visible": ["EMA20", "EMA50", "EMA200", "VWAP", "RSI", "MACD", "Volume"],
    "viewport": "1920x1080",
    "full_page": true,
    "image_path": "data/screenshots/{capture_id}.png",
    "image_size_bytes": null,
    "image_hash": "sha256:...",
    "trigger_type": "scheduled|price|volume|liquidity|macro|screener",
    "trigger_value": null
  },

  "analysis": {
    "analysis_id": "uuid",
    "analysis_timestamp_utc": "2026-05-29T00:00:10Z",
    "analysis_version": "v1",
    "analysis_method": "llm_vision|ocr|heuristic|hybrid",
    "status": "done|pending|failed",
    "error": null,
    "summary": "BTC teste une résistance avec volume en hausse.",
    "signals": [
      {
        "type": "breakout_attempt",
        "direction": "bullish",
        "confidence": 0.68,
        "evidence": ["price above VWAP", "volume increasing", "RSI rising"]
      }
    ],
    "levels": {
      "support": [104000, 102800],
      "resistance": [106500, 108000]
    },
    "trend": {
      "direction": "bullish",
      "structure": "HH/HL",
      "strength": "moderate"
    },
    "momentum": {
      "rsi": 62,
      "macd": "bullish_cross",
      "state": "rising"
    },
    "volatility": {
      "state": "normal",
      "atr_percent": 0.8
    },
    "risk_flags": ["funding elevated", "liquidity above current price"],
    "context": {
      "dxy_trend": "bearish",
      "gold_trend": "bullish",
      "oil_trend": "neutral"
    },
    "next_watch": "confirmation above resistance or rejection back below VWAP"
  },

  "setup": null,

  "distribution": {
    "telegram": {
      "sent": true,
      "message_preview": "BTCUSDT (15m) — Breakout attempt...",
      "sent_at_utc": "2026-05-29T00:00:15Z"
    },
    "deskpro": {
      "ready": true,
      "ingested_at_utc": null,
      "view_url": null
    }
  },

  "image_refs": {
    "raw": "data/screenshots/{capture_id}.png",
    "annotated": null,
    "thumbnail": null
  },

  "tags": ["BTC", "breakout", "volume", "funding_watch"],
  "pipeline_duration_ms": 15000
}
```

## 4_ENDPOINTS_DATA_CENTER

| Endpoint | Payload | Méthode |
|----------|---------|---------|
| `POST /dc/ingest/vision/raw` | `raw_capture` | Envoi immédiat après capture |
| `POST /dc/ingest/vision/analysis` | `extracted_signal` | Envoi immédiat après analyse |
| `POST /dc/ingest/vision/summary` | `generated_summary` | Envoi si analyse significative |
| `POST /dc/ingest/vision/distribution` | `distribution_payload` | Envoi après distribution Telegram |

## 5_RETRY_POLICY

- Retry : max 3 tentatives, intervalle 5s
- Timeout : 10s par requête
- Fallback : écriture locale dans `data/dc_fallback/` si Data Center indisponible
- Replay : script de rejeu depuis `data/dc_fallback/`

## 6_VOLUMETRIE_ESTIMEE

| Échelon | Captures/jour | Payloads/jour | Stockage images/jour |
|---------|---------------|---------------|---------------------|
| Minimum (scheduled only) | ~50 | ~200 | ~200 MB |
| Moyen (scheduled + triggers) | ~200 | ~800 | ~800 MB |
| Maximum (tous triggers) | ~500 | ~2000 | ~2 GB |

## 7_RETENTION_DATA_CENTER

| Type | Rétention | Archive |
|------|-----------|---------|
| Images raw | 7 jours | Optionnel S3/GCS |
| Analyses JSON | 30 jours | 90 jours |
| Setups | 90 jours | 1 an |
| Distribution logs | 30 jours | 90 jours |
