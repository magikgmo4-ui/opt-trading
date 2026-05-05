---
doc_id: SIGNAL_DIAG_01_ENDPOINTS
doc_type: endpoint_checks
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_ENDPOINT_SAFE_CHECKS

## Local

| Endpoint | Method | HTTP | Notes |
| --- | --- | --- | --- |
| /docs | GET | 200 | FastAPI Swagger UI |
| /openapi.json | GET | 200 | OpenAPI schema |
| /health | GET | 404 | NOT IMPLEMENTED |
| /tv | GET | 405 | POST-only (correct) |
| / | GET | 404 | No root |

## Public (via ngrok)

| Endpoint | HTTP | Notes |
| --- | --- | --- |
| /docs | 200 | Accessible depuis internet |
| / | 404 | Pas de root |
| server | uvicorn | Confirme |

## Perf

| Endpoint | HTTP | Notes |
| --- | --- | --- |
| /perf/open | 200 | 2 trades ouverts visibles |
| /perf/summary | 200 | Stats globales |

## Constats

- /tv accepte uniquement POST (405 for GET) — correct
- /health manquant — empeche monitoring automatique
- /docs et /openapi.json accessibles publiquement
- Serveur uvicorn confirme derriere ngrok
