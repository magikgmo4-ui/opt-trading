---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01_BOT_VISION_HEADLESS_CONTRACT
doc_type: data_contract
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_BOT_VISION_HEADLESS_CONTRACT

## Contrat `vision_context.coinglass.v1`

### Payload minimal

```json
{
  "contract_version": "v1",
  "input_class": "vision_context.coinglass.v1",
  "source_id": "coinglass_headless_bot",
  "screenshot_ts": "2026-05-23T06:00:00Z",
  "symbol": "BTCUSDT",
  "timeframe": "1H",
  "board": "liquidations",
  "page": "liquidation_heatmap",
  "freshness_state": "fresh",
  "detections": [
    {
      "detected_metric_type": "liquidations_long",
      "extracted_value": 48500000.0,
      "unit": "USD",
      "confidence": 0.82,
      "evidence_ref": "data/vision/coinglass/raw/screenshot_20260523_060000.png",
      "notes": "OCR from liquidation bar chart — value readable"
    },
    {
      "detected_metric_type": "liquidations_short",
      "extracted_value": 21300000.0,
      "unit": "USD",
      "confidence": 0.78,
      "evidence_ref": "data/vision/coinglass/raw/screenshot_20260523_060000.png",
      "notes": "OCR from liquidation bar chart — value readable"
    }
  ],
  "warnings": [],
  "refs": {
    "raw_screenshot": "data/vision/coinglass/raw/screenshot_20260523_060000.png",
    "normalized": "data/vision/coinglass/normalized/vision_20260523_060000.json",
    "latest": "data/vision/coinglass/latest.json",
    "events": "data/vision/coinglass/events.jsonl"
  }
}
```

### Champs requis

| Champ | Type | Requis | Description |
|---|---|---|---|
| `contract_version` | string | oui | `"v1"` |
| `input_class` | string | oui | `"vision_context.coinglass.v1"` |
| `source_id` | string | oui | identifiant du bot |
| `screenshot_ts` | string | oui | timestamp UTC Z du screenshot |
| `symbol` | string | oui | symbole cible |
| `timeframe` | string | oui | timeframe de la vue Coinglass |
| `board` | string | oui | tableau consulté |
| `page` | string | oui | page/vue exacte |
| `freshness_state` | string | oui | `fresh`, `stale`, `unknown` |
| `detections` | list | oui | liste des métriques détectées |
| `detections[].detected_metric_type` | string | oui | nom de la métrique |
| `detections[].extracted_value` | float ou null | oui | valeur extraite, null si non lisible |
| `detections[].unit` | string | oui | unité (USD, %, ratio) |
| `detections[].confidence` | float [0,1] | oui | confiance de l'extraction |
| `detections[].evidence_ref` | string | oui | chemin du screenshot source |
| `detections[].notes` | string | non | raison d'une valeur null ou incertitude |
| `warnings` | list | non | avertissements globaux |
| `refs` | object | oui | pointeurs fichiers |

### Invariants

1. `extracted_value = null` si la valeur n'est pas lisible dans le screenshot.
2. `confidence < 0.5` → `warnings` doit contenir un avertissement de confiance basse.
3. Aucune valeur ne doit être inventée ou interpolée depuis une source externe.
4. `input_class` est toujours `"vision_context.coinglass.v1"` — jamais `"market_metrics.v1"`.
5. Le bot ne touche pas aux fichiers `data/derivatives/` ni `data/deskpro/inputs/market_metrics/`.

### Métriques cibles Coinglass

| detected_metric_type | Board Coinglass | Notes |
|---|---|---|
| `liquidations_long` | Liquidations | Valeur USD des longs liquidés |
| `liquidations_short` | Liquidations | Valeur USD des shorts liquidés |
| `long_short_ratio` | Long/Short Ratio | Ratio brut ou pourcentage |
| `open_interest` | Open Interest | USD ou BTC |
| `liquidation_heatmap_level` | Heatmap | Niveau de prix à forte liquidation |

### Confidence thresholds

| Seuil | Signification |
|---|---|
| ≥ 0.85 | Valeur fiable — utilisable pour context Desk Pro |
| 0.60 – 0.84 | Valeur probable — à signaler avec warning |
| < 0.60 | Valeur incertaine — null recommandé |

### Desk Pro input path

```text
data/deskpro/inputs/vision_context/coinglass/latest.json
```

Desk Pro lit ce fichier en read-only, indépendamment de `data/deskpro/inputs/market_metrics/latest.json`.
