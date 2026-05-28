# 10_OBSERVABILITY_SPEC

## Métriques

| Métrique | Description |
|---|---|
| `data_center.writes.total` | Nombre total d'écritures |
| `data_center.reads.total` | Nombre total de lectures |
| `data_center.errors.total` | Nombre d'erreurs |
| `data_center.schema_validations.ok` | Validations OK |
| `data_center.schema_validations.fail` | Validations échouées |

## Logs

Chaque événement dans `events.jsonl` doit contenir : `timestamp`, `event_type`, `producer_id`, `status`, `message`.

## Alertes

| Condition | Action |
|---|---|
| `errors > 5 en 1min` | Alerte Telegram |
| `schema_validation fail rate > 10%` | Alerte Telegram |
| `disk usage > 90%` | Alerte Telegram |

## Healthcheck

`GET /health` → `{"status": "ok", "uptime": ..., "last_write": ..., "error_count": ...}`
