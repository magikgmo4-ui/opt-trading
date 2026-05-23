---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01_DATA_FLOW_AND_STORAGE_PLAN
doc_type: data_flow_plan
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 30_DATA_FLOW_AND_STORAGE_PLAN

## Flux de données

```text
[Interface Coinglass]
      |
      | (headless browser capture)
      v
[Bot vision headless]
      |
      | screenshot PNG + OCR/vision extraction
      v
[vision_context.coinglass.v1 payload]
      |
      +---> data/vision/coinglass/raw/screenshot_YYYYMMDD_HHMMSS.png
      +---> data/vision/coinglass/normalized/vision_YYYYMMDD_HHMMSS.json
      +---> data/vision/coinglass/latest.json                (écrasé à chaque run)
      +---> data/vision/coinglass/events.jsonl               (append-only)
      +---> data/deskpro/inputs/vision_context/coinglass/latest.json  (Desk Pro input)
```

## Chemins de stockage

### Raw captures

```text
data/vision/coinglass/raw/
  screenshot_YYYYMMDD_HHMMSS.png     — screenshot brut
  screenshot_YYYYMMDD_HHMMSS.meta.json — metadata de capture (URL, viewport, board)
```

### Normalized outputs

```text
data/vision/coinglass/normalized/
  vision_YYYYMMDD_HHMMSS.json        — payload vision_context.coinglass.v1 complet
```

### Latest (Desk Pro input)

```text
data/vision/coinglass/latest.json                          — dernière vision_context.v1
data/deskpro/inputs/vision_context/coinglass/latest.json   — copie pour Desk Pro read-only
```

### Event log

```text
data/vision/coinglass/events.jsonl   — append-only ; chaque run → une ligne JSON
```

Format event line :
```json
{"ts": "2026-05-23T06:00:00Z", "symbol": "BTCUSDT", "board": "liquidations", "detections_count": 2, "max_confidence": 0.82, "freshness_state": "fresh"}
```

### Status

```text
data/vision/coinglass/status.json
```

```json
{
  "last_run_ts": "2026-05-23T06:00:00Z",
  "last_symbol": "BTCUSDT",
  "last_board": "liquidations",
  "last_freshness": "fresh",
  "run_count": 12,
  "error_count": 0
}
```

## Séparation des surfaces

| Surface | Chemin | Producteur | Consommateur |
|---|---|---|---|
| `market_metrics.v1` | `data/derivatives/` | derivatives_collector API | Desk Pro, Perf |
| `vision_context.coinglass.v1` | `data/vision/coinglass/` | bot vision headless | Desk Pro (futur) |

Ces deux surfaces ne se fusionnent pas. Desk Pro lira deux inputs distincts.

## Règles de rétention

- Screenshots raw : rotation après 7 jours (ou selon capacité disque)
- Normalized : garder les 30 derniers runs
- `latest.json` : toujours le plus récent
- `events.jsonl` : rotation mensuelle
- `status.json` : mis à jour à chaque run

## Invariants stockage

- Aucun write dans `data/derivatives/`
- Aucun write dans `data/deskpro/inputs/market_metrics/`
- Desk Pro lit `vision_context/coinglass/latest.json` en read-only
- Le bot ne modifie pas les fichiers du collector API
