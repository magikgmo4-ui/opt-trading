---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LOCALCMS_HEALTH_READER_01_INVENTORY
doc_type: inventory
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LOCALCMS_HEALTH_READER_01
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_LOCALCMS_HEALTH_INVENTORY

## Consumer `localcms__data_center_health` — état avant GO

| Champ | Valeur |
|---|---|
| `implementation_status` | `not_started` |
| `contract_class` | `null` |
| `access_pattern` | `status_only` |
| `read_path` | `data/data_center/_registry/producers.json` |
| `fallback` | `silent_empty` |

Aucun reader Python ni endpoint LocalCMS n'existaient.

## Surface LocalCMS — état avant GO

`modules/localcms/app/main.py` — FastAPI port 8700, endpoints existants :

| Endpoint | Description |
|---|---|
| `GET /health` | LocalCMS service health |
| `GET /menu` | Menu JSON |
| `GET /menu/state` | Module state cache |
| `GET /runtime/tmux` | TMUX sessions report |
| `GET /runtime/tmux/live` | Live TMUX session list |
| `GET /metrics/daily` | Métriques daily JSON |
| `GET /metrics` | Dashboard HTML |
| `GET /journal/daily` | Journal entries |

Aucun endpoint Data Center n'existait.

## Reader — conception

`read_data_center_health()` dans `modules/data_center/localcms_health_reader.py` :

- Appelle `load_producers_registry()` et `load_consumers_registry()` depuis `modules.data_center.layout`
- Retourne : `ok`, `consumer_id`, `source`, `producer_count`, `consumer_count`, `implemented_consumers`, `not_started_consumers`, `contract_classes`, `warnings`, `read_at`
- Aucun accès à `data/` — lecture registry statique uniquement

## Endpoint — conception

`GET /data-center/health` dans `modules/localcms/app/main.py` :
- Import lazy de `read_data_center_health` (évite la dépendance circulaire au startup)
- Retourne `JSONResponse(content=read_data_center_health())`

## Récapitulatif consommateurs après GO

| Consumer | implementation_status | Reader réel |
|---|---|---|
| `desk_pro__market_metrics` | `implemented` | `modules/desk_pro/service/market_metrics_reader.py` |
| `localcms__data_center_health` | `implemented` | `modules/data_center/localcms_health_reader.py` |
| `desk_pro__spot_snapshot` | `not_started` | Non |
| `strategy_framework__market_context` | `not_started` | Non |
| `perf_engine__replay_context` | `not_started` | Non |
| `telegram_screener__signal_context` | `not_started` | Non |
| `google_sheets__market_reporting` | `not_started` | Non |
