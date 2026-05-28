# 10_CONSUMER_CONTRACTS_SPEC

## Consumer contracts

| Surface | Format lecture | Latence | Endpoint/Path | Fallback |
|---|---|---|---|---|
| PF_DESK_PRO | JSON via API | < 1s | `GET /api/v1/market-data/{symbol}` | Cache local |
| PF_STRATEGY_FRAMEWORK_REGISTRY | JSON via filesystem | < 5s | `data/data_center/<producer>/latest.json` | Dernier snapshot |
| PF_PERF_ENGINE_TRADING_LAB | JSON via filesystem | < 10s | `data/data_center/perf/` | Données perf directes |
| PF_TELEGRAM_SCREENER | JSON via filesystem | < 30s | `data/data_center/screener/` | Dernier signal |
| PF_TELEGRAM_INGESTION | JSON via filesystem | < 30s | `data/data_center/ingestion/` | File d'attente |
| PF_GOOGLE_SHEETS_CONSUMER | JSON via API | < 60s | `GET /api/v1/sheets/{sheet}` | Cache Google Sheets |
| PF_LOCALCMS_COCKPIT | JSON via filesystem | < 5s | `data/data_center/health/` | Dernière santé connue |

## Module structure

```text
modules/data_center/
  consumers/
    __init__.py
    consumer_registry.py
    consumer_router.py
    desk_pro_adapter.py
    sheets_adapter.py
    localcms_adapter.py
  tests/
    test_consumer_registry.py
    test_consumer_router.py
```
