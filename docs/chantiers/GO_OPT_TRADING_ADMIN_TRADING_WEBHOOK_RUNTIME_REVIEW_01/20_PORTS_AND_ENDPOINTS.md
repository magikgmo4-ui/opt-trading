---
doc_id: WEBHOOK_REVIEW_01_PORTS
doc_type: ports_endpoints
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_PORTS_AND_ENDPOINTS

## Listeners

| Port | Interface | Process | Service |
| --- | --- | --- | --- |
| 8000 | 0.0.0.0 | python (PID 1466, ghost) | tv-webhook |
| 8010 | 0.0.0.0 | python (PID 796, root) | tv-perf |
| 4040 | 127.0.0.1 | ngrok (PID 1492, ghost) | ngrok API |

## Endpoints testes (safe, read-only)

| Endpoint | Port | Code | Resultat |
| --- | --- | --- | --- |
| GET /health | 8000 | 404 | **NOT IMPLEMENTED** |
| GET /docs | 8000 | 200 | FastAPI Swagger UI |
| GET /perf/open | 8010 | 200 | 2 open trades (BITGET_SM_LITE, COINM_SHORT) |
| GET /perf/summary | 8010 | 200 | Stats: 4564 trades, 60% WR, -84K PnL |
| GET /api/tunnels | 4040 | 200 | ngrok tunnel info |

## Endpoints non testes (dangereux)

| Endpoint | Port | Raison |
| --- | --- | --- |
| POST /tv | 8000 | Webhook TradingView — declenche trades |
| POST /perf/event | 8010 | Ecriture evenement perf |
| POST /webhook | 8000 | Alias webhook |
| GET /dash | 8000 | Dashboard HTML (safe mais non teste) |

## Perf data

```
total_trades: 4564
open_trades: 2 (BITGET_SM_LITE XAUUSDT LONG + COINM_SHORT BTCUSDT SHORT)
winrate: 60.04%
pnl_realized: -84,255
equity_last: -74,255
max_dd: 1,650,899 (16509%)
engines: PAPER_TEST, COINM_SHORT, BITGET_SM_LITE
```

## Securite

- 8000 et 8010 exposes sur 0.0.0.0 (toutes interfaces)
- tv-webhook EnvironmentFile expose .env via variables d'environnement
- ngrok expose /tv publiquement (via URL ngrok)
- Aucun /health endpoint pour monitoring
- tv-perf tourne en root (inutilement)
