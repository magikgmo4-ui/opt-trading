---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01_DATA_CENTER
doc_type: data_center_ingestion
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01
---

# 05_DATA_CENTER_INGESTION.md

Schéma d'ingestion maximum vers Data Center.

## 1_PRINCIPES

- Data Center reçoit le maximum de données structurées (pas de filtre émetteur)
- Distinguer 4 catégories : raw_capture / extracted_signal / generated_summary / distribution_payload
- Chaque payload est autonome (capture_id + timestamp + source)
- Le chemin canonique Data Center est `data/data_center/views/vision/` (pas `data/deskpro/inputs/`)

## 2_CATEGORIES_DE_PAYLOAD

| Catégorie | Contenu | Source |
|-----------|---------|--------|
| `raw_capture` | Métadonnées de capture (sans image) | capture_headless.js |
| `extracted_signal` | Signaux extraits par analyseur | bot_vision_step2 / OCR |
| `generated_summary` | Résumé texte + niveaux | bot_vision_step2 |
| `distribution_payload` | Payload complet distribuable | Adapter vers DeskPro |

## 3_SCHEMA_MAX_DATA_OUT

```json
{
  "payload_id": "uuid",
  "payload_type": "raw_capture|extracted_signal|generated_summary|distribution_payload",
  "pipeline_version": "v1",
  "capture": {
    "capture_id": "uuid",
    "timestamp_utc": "2026-05-29T00:00:00Z",
    "source": "tradingview",
    "screen_type": "CHART_TECHNICAL",
    "asset": "BTCUSDT",
    "asset_class": "crypto",
    "timeframe": "15m",
    "url_key": "tradingview_btcusdt_15m",
    "indicators_visible": ["EMA20", "EMA50", "VWAP"],
    "layout": "single",
    "trigger_type": "scheduled",
    "image_path": "data/screenshots/{capture_id}.png",
    "image_hash": "sha256:..."
  },
  "analysis": {
    "analysis_id": "uuid",
    "analysis_version": "v1",
    "analysis_method": "openai_vision|ocr|heuristic",
    "status": "done",
    "summary": "BTC teste résistance avec volume.",
    "signals": [],
    "levels": {
      "support": [104000, 102800],
      "resistance": [106500, 108000]
    },
    "trend": {
      "direction": "bullish",
      "structure": "HH/HL",
      "strength": "moderate"
    },
    "risk_flags": ["funding elevated"]
  },
  "distribution": {
    "telegram": {"sent": true, "message_preview": "..."},
    "deskpro": {"ready": true, "ingested_at_utc": null}
  }
}
```

## 4_ENDPOINTS_DATA_CENTER

| Endpoint | Payload | Priorité |
|----------|---------|----------|
| `POST /dc/ingest/vision/raw` | raw_capture metadata | P1 |
| `POST /dc/ingest/vision/analysis` | extracted_signal | P1 |
| `POST /dc/ingest/vision/summary` | generated_summary | P2 |
| `POST /dc/ingest/vision/distribution` | distribution_payload | P2 |

Note : les endpoints Data Center n'existent pas encore. Première version = écriture fichier local dans `data/data_center/views/vision/`.

## 5_CHEMINS_CANONIQUES

| Donnée | Chemin canonique | Priorité |
|--------|-----------------|----------|
| Capture brute | `data/screenshots/{capture_id}.png` | P0 |
| Métadonnées capture | `data/screenshots/{capture_id}.json` | P0 |
| Analyse vision | `data/deskpro/vision/runs/<id>/summary.json` | P0 (via bot_vision_step2) |
| Vision analysis v1 | `data/deskpro/inputs/vision_analysis/latest.json` | P1 (via adapter) |
| Snapshot DeskPro | `/opt/trading/desk/snapshots/latest.json` | P0 (via desk_snapshot_ingest) |
| Data Center view | `data/data_center/views/vision/latest.json` | P2 (futur) |

## 6_RETENTION

| Type | Rétention | Nettoyage |
|------|-----------|-----------|
| Images raw | 7 jours | bot_vision_step2 prune |
| Analyses JSON | 30 jours | bot_vision_step2 prune |
| Snapshots DeskPro | 7 jours | desk_retention |
| Data Center views | 90 jours | À définir |
