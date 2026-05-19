---
go_id: GO_OPT_TRADING_DESKPRO_RUNTIME_ALERT_DISPATCH_01
doc_type: initial_project_doc
repo: opt-trading
status: DRAFT
created_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_RUNTIME_ALERT_DISPATCH_01

## 1_MASTER_TARGET

Passer de l'état de santé visible à une alerte actionnable avec cooldown anti-spam, journalisation, endpoint dédié et affichage UI.

## 10_IMPLEMENTATION

### routes.py

- `ALERT_COOLDOWN_SEC` (env, default 300s)
- `ALERTS_JSONL` → `/opt/trading/tmp/desk_pro_alerts.jsonl`
- `_alert_state` in-memory: last_status, last_ts, cooldown_until
- `_check_alert(health_status)` → triggered/cooldown/healthy
- `_read_alerts(limit)` → read last N from JSONL
- `/desk/status` → `alert` field
- `GET /desk/alerts` → state + history

### page.py

- Alert bar in Pipeline Status card (triggered = orange, cooldown = muted)

## 13_ESTABLISHED

- Health state: healthy/degraded/down from PR #550
- Cooldown: 300s default, configurable via env
- Alerts persisted to JSONL
- 322/322 PASS
