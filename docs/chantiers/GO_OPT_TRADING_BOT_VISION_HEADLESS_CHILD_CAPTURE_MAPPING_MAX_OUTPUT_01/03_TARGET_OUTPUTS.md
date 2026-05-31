# 03 — Target Outputs

## Outputs pipeline

| Output | Format | Producer | Consumer |
|--------|--------|----------|----------|
| capture_metadata.json | JSON (sidecar) | capture_headless.js | desk_snapshot_ingest, vision_analysis_writer |
| vision_analysis.v1 | JSON (latest.json) | vision_analysis_writer.py | DeskPro vision_analysis_reader, Data Center |
| deskpro_input.json | JSON (latest.json) | vision_analysis_writer.py | DeskPro UI |
| data_center_ingest.jsonl | JSONL | vision_analysis_writer.py | Data Center views |
| telegram_summary.json | JSON | telegram_filter.py | shared/telegram_notify.py |
| summary.json | JSON | bot_vision_step2.py | vision_analysis_writer.py |
| analysis.txt / analysis.md | Text/Markdown | bot_vision_step2.py | vision_outbox |

## Chemin DeskPro

```
data/deskpro/inputs/vision_analysis/latest.json
```

Format : `vision_analysis.v1` — voir fixture `tests/fixtures/capture_mapping/vision_analysis_v1_sample.json`

## Chemin Data Center

```
data/data_center/views/vision_analysis/latest.json          # Vue contract neutre
data/data_center/views/vision_analysis/by_symbol/<SYMBOL>.json  # Par symbole
data/data_center/views/vision_analysis/history/<SYMBOL>_<run>.json  # Historique
```

Format : `vision_analysis.v1` — identique au DeskPro, copié atomiquement.

## Schémas existants réutilisés

- `visual_context.v1` → modules/desk_pro/visual_context_adapter.py
- `desk_snapshot.v1` → modules/desk_pro/desk_snapshot_adapter.py
- `market_metrics.v1` → modules/derivatives_collector/app/market_metrics_v1.py
- `vision_analysis.v1` → modules/desk_pro/service/vision_analysis_reader.py

## Contrat vision_analysis.v1

Champ requis :
- `input_class` : MUST be "vision_analysis.v1"
- `capture_id` : unique ID
- `symbol` : asset symbol
- `timeframe` : timeframe
- `analysis_ts` : ISO timestamp
- `source_module` : producer name
- `freshness_state` : "fresh" | "stale" | "unknown"
- `signals` : array of {type, value, confidence, note}
