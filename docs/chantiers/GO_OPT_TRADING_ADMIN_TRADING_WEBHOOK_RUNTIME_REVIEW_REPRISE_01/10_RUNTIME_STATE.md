---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01_RUNTIME_STATE
doc_type: runtime_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 10_RUNTIME_STATE - Webhook Runtime State

## Commandes executees

```bash
systemctl status tv-webhook.service --no-pager || true
systemctl status tv-perf.service --no-pager || true
systemctl status ngrok-tv.service --no-pager || true
ss -ltnp | grep -E '(:8000|:8010|:4040)' || true
```

## Resultat observe

### tv-webhook

- `tv-webhook.service` est `active (running)`
- process principal observe: `python -m uvicorn webhook_server:app --host 0.0.0.0 --port 8000`
- service charge depuis `/etc/systemd/system/tv-webhook.service`
- statut observe sans restart ni reload

### Activite observee dans le statut systemd

- des `POST /tv` locaux `127.0.0.1` ont ete visibles avec melange de `200 OK` et `400 Bad Request`
- un `GET /api/metrics` local `127.0.0.1` a aussi ete visible en `200 OK`
- ce GO ne conclut pas a l'origine metier de ces appels; il constate seulement une activite locale recente sur la surface webhook

### tv-perf

- `tv-perf.service` est `active (running)`
- process principal observe: `python -m uvicorn perf.perf_app:app --host 0.0.0.0 --port 8010`
- des `GET /perf/summary` et `POST /perf/event` locaux en `200 OK` sont visibles dans le statut
- `tv-perf` est donc un voisin runtime actif du webhook, sans etre le producteur principal audite ici

### ngrok-tv

- `ngrok-tv.service` est `active (running)`
- commande observee: `ngrok http 8000`
- le tunnel public n'a pas ete sollicite par ce GO
- des erreurs transitoires de reconnexion DNS/egress sont visibles dans les journaux exposes par `systemctl status`, puis une session a ete retablie

### Ports runtime

- `0.0.0.0:8000` -> `tv-webhook`
- `0.0.0.0:8010` -> `tv-perf`
- `127.0.0.1:4040` -> UI locale `ngrok`

## Lecture runtime retenue

- la surface webhook est reellement active et observable en read-only
- le webhook n'est pas idle au moment de cette reprise, contrairement a l'ancien chantier clos sur la branche stale
- la surface TradingView externe n'a pas ete testee; seule l'observabilite locale a ete confirmee

## Side effects

NONE
