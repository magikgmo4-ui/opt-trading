---
doc_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_CHILD_GATEWAY_START_SMOKE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_CHILD_GATEWAY_START_SMOKE_01
parent_go: GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_PARENT_01
status: closed
lifecycle_stage: cadrage
created_at: 2026-05-31
machine: db-layer
---

# 00_INITIAL_PROJECT_DOC — Child : Gateway Start Smoke

## 1_MASTER_TARGET

Démarrer le gateway OpenClaw sur db-layer (tmux `openclaw-gateway`),
prouver la reachability WebSocket sur `ws://127.0.0.1:18789`,
et valider le health check (agents disponibles, Telegram ok).

## 2_COMMANDES_REFERENCE

```bash
# Démarrer
sudo -u openclaw tmux new-session -d -s openclaw-gateway \
  "openclaw gateway run --bind loopback --port 18789"

# Health
sudo -u openclaw openclaw health

# Probe
sudo -u openclaw openclaw gateway status
```

## 3_CRITERES_PASS

| Critère | Requis |
| --- | --- |
| tmux session openclaw-gateway | présente |
| gateway listening 127.0.0.1:18789 | oui |
| RPC probe | ok |
| health : agents listés | >= 1 |
| health : Telegram | ok |
