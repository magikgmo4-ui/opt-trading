---
go_id: GO_OPT_TRADING_DESKPRO_RUNTIME_ALERTING_AND_HEALTH_BADGES_01
doc_type: initial_project_doc
repo: opt-trading
status: DRAFT
created_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_RUNTIME_ALERTING_AND_HEALTH_BADGES_01

## 1_MASTER_TARGET

Passer de *voir l'état* à *être alerté/actionnable* : badge santé agrégé (healthy/degraded/down) avec seuils configurables, visible dans Desk Pro UI.

## 3_INITIAL_NEED

PR #544 + #547 livrent l'observabilité complète (status, sources, erreurs) mais sans agrégation santé ni seuils.

## 5_AUDIT — EXISTANT

| Élément | Source |
|---|---|
| `INACTIVITY_SEC_DEFAULT` (1h) | webhook_server.py L86 |
| Status "STALE" / "OK" per engine | webhook metrics L409 |
| `last_event_age_sec` in metrics | webhook metrics L428 |
| `last_event_ts` in perf summary | perf_app.py |
| `_desk_errors` FIFO | routes.py L17 |
| Telegram bot token + send | webhook_server L82, L262 |
| source modes (live/fixture/mock) | routes.py _source_mode |

## 10_IMPLEMENTATION

### routes.py

Ajouter `_compute_health(status_data: dict) -> dict` :

```python
def _compute_health(d: dict) -> dict:
    checks = []
    errors = []

    # 1. Webhook reachable
    wh = d.get("webhook")
    if wh is None:
        checks.append({"check": "webhook", "status": "fail", "reason": "unreachable"})
    else:
        checks.append({"check": "webhook", "status": "pass"})

    # 2. Perf reachable
    perf = d.get("perf")
    if perf is None:
        checks.append({"check": "perf", "status": "fail", "reason": "unreachable"})
    else:
        checks.append({"check": "perf", "status": "pass"})

    # 3. Webhook event age
    whm = d.get("webhook_metrics") or {}
    age = whm.get("last_event_age_sec")
    if age is None:
        checks.append({"check": "webhook_age", "status": "warn", "reason": "no events yet"})
    elif age > 7200:
        checks.append({"check": "webhook_age", "status": "fail", "reason": f"{age}s since last event"})
    elif age > 3600:
        checks.append({"check": "webhook_age", "status": "warn", "reason": f"{age}s since last event"})
    else:
        checks.append({"check": "webhook_age", "status": "pass"})

    # 4. Error count
    ec = d.get("error_count", 0)
    if ec > 20:
        checks.append({"check": "errors", "status": "fail", "reason": f"{ec} probe errors"})
    elif ec > 5:
        checks.append({"check": "errors", "status": "warn", "reason": f"{ec} probe errors"})
    else:
        checks.append({"check": "errors", "status": "pass"})

    # 5. Source modes
    sources = d.get("sources") or {}
    for k, v in sources.items():
        if v == "down":
            checks.append({"check": f"source_{k}", "status": "fail", "reason": f"source {v}"})

    has_fail = any(c["status"] == "fail" for c in checks)
    has_warn = any(c["status"] == "warn" for c in checks)

    if has_fail:
        overall = "down"
    elif has_warn:
        overall = "degraded"
    else:
        overall = "healthy"

    return {"status": overall, "checks": checks}
```

### /desk/status

Ajouter champ `health` dans le retour.

### page.py

Pipeline Status card :
- Badge santé en haut (vert = healthy, orange = degraded, rouge = down)
- Détail des checks dans une table
- Garder le raw JSON en `<details>`

## 13_ESTABLISHED

- `INACTIVITY_SEC_DEFAULT` = 3600s (webhook_server.py L86)
- `telegram_send()` existe (webhook_server.py L262)
- `_desk_errors` FIFO dans routes.py
- `_source_mode` distingue live/fixture/mock

## 16_TODO

1. Implémenter `_compute_health` dans routes.py
2. Intégrer dans `/desk/status`
3. UI : badge santé + checks table
4. Tests 322/322 PASS
5. PR
