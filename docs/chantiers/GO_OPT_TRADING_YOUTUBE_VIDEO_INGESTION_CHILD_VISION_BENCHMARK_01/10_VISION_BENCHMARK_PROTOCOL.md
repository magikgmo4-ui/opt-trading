# Vision Benchmark Protocol

## Inputs

```text
outputs/youtube/pilots/trademachineoff/parser_input/*.json
```

Chaque fichier doit contenir au minimum :

```text
video_id
screen_text
ocr_segments
vision
```

Si `vision` manque, le benchmark recalcule Vision Layer V1 depuis
`screen_text` + `ocr_segments`.

## OCR prerequisites

Sur Windows, le benchmark réel nécessite que les outils vidéo/OCR soient
installés et disponibles dans le `PATH`, ou qu'une commande OCR custom soit
fournie.

Pré-requis usuels :

```text
yt-dlp
ffmpeg
tesseract
```

PowerShell doit toujours quoter le handle source :

```bash
--source '@trademachineoff'
```

Run OCR configurable :

```bash
python -m modules.youtube_video_ingestion.cli \
  --source '@trademachineoff' \
  --limit 50 \
  --output outputs/youtube/pilots/trademachineoff_real_ocr \
  --subtitle-lang en \
  --enable-ocr \
  --frame-rate 1 \
  --ocr-command "tesseract {image} stdout -l eng" \
  --parsed-jsonl outputs/youtube/parsed/trademachineoff_real_ocr.jsonl
```

La commande OCR doit inclure le placeholder `{image}`. Le stdout devient le
texte OCR de la frame. Un exit non-zero est capturé dans `ocr_error_summary` et
ne bloque pas le batch.

## Annotation template

Commande locale :

```bash
python -m modules.youtube_video_ingestion.cli benchmark-vision-template \
  --parser-input-dir outputs/youtube/pilots/trademachineoff/parser_input \
  --output outputs/youtube/benchmark/trademachineoff_annotations_template.json \
  --limit 50
```

Le template pré-remplit les prédictions Vision V1. Elles doivent être relues et
corrigées manuellement avant scoring.

## Annotation schema

```json
{
  "schema_version": "vision_benchmark_annotations_v1",
  "annotations": [
    {
      "video_id": "example",
      "expected": {
        "symbols": ["XAUUSD"],
        "prices": [{"role": "entry", "value": 2345.0}],
        "timeframes": ["M5"],
        "indicators": ["EMA"],
        "chart_detected": true
      },
      "notes": "manual review notes"
    }
  ]
}
```

## Scoring

Commande locale :

```bash
python -m modules.youtube_video_ingestion.cli benchmark-vision \
  --parser-input-dir outputs/youtube/pilots/trademachineoff/parser_input \
  --annotations outputs/youtube/benchmark/trademachineoff_annotations_reviewed.json \
  --output outputs/youtube/benchmark \
  --fixtures-output outputs/youtube/benchmark/fixtures_real_world \
  --limit 50
```

Résultats :

```text
outputs/youtube/benchmark/benchmark_results.json
outputs/youtube/benchmark/benchmark_report.md
outputs/youtube/benchmark/fixtures_real_world/
```

## Metrics

Le benchmark calcule :

```text
symbols: precision / recall / F1 / exact_match_rate
prices: precision / recall / F1 / exact_match_rate
timeframes: precision / recall / F1 / exact_match_rate
indicators: precision / recall / F1 / exact_match_rate
chart_detected: accuracy
```

## Commit policy

Ne pas committer `outputs/`.

Les seules données benchmark candidates au commit sont :

```text
fixtures réduites validées
rapports synthétiques
annotations sans média brut
```
