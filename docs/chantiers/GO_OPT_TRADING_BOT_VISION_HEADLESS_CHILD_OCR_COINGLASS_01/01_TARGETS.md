# 01 — Targets

## Sortie attendue

Format `vision_context.coinglass.v1` (compatible DeskPro `vision_context_reader.py`) :

```json
{
  "input_class": "vision_context.coinglass.v1",
  "symbol": "BTCUSDT.P",
  "source_id": "coinglass_headless_bot",
  "freshness_state": "fresh",
  "screen_type": "LIQUIDITY_COINGLASS",
  "detections": [
    {
      "extracted_value": 42500000,
      "detected_metric_type": "liquidations_long",
      "confidence": 0.78,
      "detection_method": "stub",
      "unit": "USD"
    }
  ]
}
```

## Métriques par screen type

| Screen type | Métriques extraites | Unité |
|-------------|-------------------|-------|
| LIQUIDITY_COINGLASS | liquidations_long, liquidations_short, liquidation_heatmap_level | USD |
| FUNDING_COINGLASS | funding_rate | rate |
| OI_COINGLASS | open_interest, open_interest_change_24h | USD |
| LS_RATIO_COINGLASS | long_short_ratio | ratio |

## Chemins de sortie

```
DeskPro : data/deskpro/inputs/vision_context/coinglass/latest.json
Data Center : data/data_center/views/vision_context/coinglass/latest.json
Data Center (hist) : data/data_center/views/vision_context/coinglass/history/<symbol>_<ts>.json
```

## Usage

```bash
# Stub (par défaut)
python3 scripts/run_vision_pipeline.py --profile profiles.coinglass.json

# Real OCR si pytesseract dispo
python3 scripts/run_vision_pipeline.py --profile profiles.coinglass.json --real-ocr

# Analyse directe
python3 scripts/coinglass_ocr_analyzer.py --sidecar /path/to/sidecar.json
python3 scripts/coinglass_ocr_analyzer.py --stdin < sidecar.json

# Publication seule
python3 scripts/vision_context_writer.py --input vision_context.json
```
