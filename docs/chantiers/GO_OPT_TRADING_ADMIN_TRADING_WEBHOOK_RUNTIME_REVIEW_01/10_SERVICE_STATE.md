---
doc_id: WEBHOOK_REVIEW_01_SERVICE
doc_type: service_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_SERVICE_STATE — Webhook Runtime

## tv-webhook.service

| Propriete | Valeur |
| --- | --- |
| Status | active (running since Apr 19) |
| PID | 1466 |
| User | ghost |
| Port | 0.0.0.0:8000 |
| WDir | /opt/trading |
| ExecStart | /opt/trading/venv/bin/python -m uvicorn webhook_server:app --host 0.0.0.0 --port 8000 |
| EnvFile | /opt/trading/.env |
| Restart | always, 2s |
| Override | /etc/systemd/system/tv-webhook.service.d/override.conf |
| /health | 404 (NOT IMPLEMENTED) |
| /docs | 200 (FastAPI docs exposed) |
| /dash | 200 (dashboard, seen in logs) |

## tv-perf.service

| Propriete | Valeur |
| --- | --- |
| Status | active (running since Apr 19) |
| PID | 796 |
| User | **root** |
| Port | 0.0.0.0:8010 |
| WDir | /opt/trading |
| ExecStart | /opt/trading/venv/bin/python -m uvicorn perf.perf_app:app --host 0.0.0.0 --port 8010 |
| EnvFile | **AUCUN** (charge .env implicitement via load_env()) |
| Restart | always, 1s |
| /perf/open | 200 (liste trades ouverts) |
| /perf/summary | 200 (stats globales) |

## ngrok-tv.service

| Propriete | Valeur |
| --- | --- |
| Status | active (running since Apr 19) |
| PID | 1492 |
| User | ghost |
| Port | 127.0.0.1:4040 (API) |
| Target | http://localhost:8000 |
| Config | /home/ghost/.config/ngrok/ngrok.yml + /etc/ngrok/ngrok-secrets.yml |
| Public URL | https://phytogeographical-subnodulous-joycelyn.ngrok-free.dev |

## OpenCode

| Propriete | Valeur |
| --- | --- |
| Binary | /usr/local/bin/opencode 1.4.2 |
| Port | 127.0.0.1:4096 |
| Contexte | IDE, pas runtime trading |
