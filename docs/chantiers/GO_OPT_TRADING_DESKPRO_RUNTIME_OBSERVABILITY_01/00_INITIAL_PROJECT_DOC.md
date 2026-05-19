---
go_id: GO_OPT_TRADING_DESKPRO_RUNTIME_OBSERVABILITY_01
doc_type: initial_project_doc
repo: opt-trading
status: DRAFT
created_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_RUNTIME_OBSERVABILITY_01

## 1_MASTER_TARGET

Ajouter une observabilité centralisée du pipeline ingestion → perf → Desk Pro UI, visible depuis Desk Pro.

## 3_INITIAL_NEED

Le pipeline est validé mais opaque : aucun endpoint unique ne montre l'état complet (webhook up ? perf up ? source mode ? dernier event ?).

## 5_AUDIT — OBSERVABILITÉ EXISTANTE

### Webhook server (port 8000)

| Endpoint | Utilité |
|---|---|
| `GET /api/state` | Engine actif, last update |
| `GET /api/events` | Derniers events webhook |
| `GET /api/metrics` | Métriques agrégées |
| `GET /api/risk/status` | Risk limits, trade_allowed, daily PnL |
| `GET /api/paper/guards` | Paper test guards |

### Desk Pro (port 8010)

| Endpoint | Utilité |
|---|---|
| `GET /desk/health` | Mode step2_mock, module ok |
| `GET /desk/logs/latest` | Dernières lignes log UI |
| `GET /desk/snapshot` | Fixture/metrics actuelles |
| `GET /perf/summary` | KPIs trading |
| `GET /perf/open` | Positions ouvertes |

### Gaps

| Gap |
|---|
| Aucun endpoint ne montre le pipeline complet (webhook → perf → desk) |
| Aucun probe cross-service |
| Aucune page unifiée de status |

## 7_CANONICAL_STATE

- Desk Pro port 8010 : fixture snapshot + mock fallback
- Webhook_server port 8000 : actif avec TRADE_ALLOWED=true
- Perf SQLite : 7 trades (5 closed, 2 open)
- unittest 92/92 PASS

## 10_IMPLEMENTATION

### Endpoint ajouté : `GET /desk/status`

Nouvelle route dans `modules/desk_pro/api/routes.py` :

```json
{
  "desk_pro": {"ok": true, "mode": "step2_mock"},
  "perf": {"trades": 7, "closed": 5, "open": 2, "pnl": 540},
  "webhook": {"ok": true, "trade_allowed": true, "active_engine": null},
  "sources": {
    "snapshot": "fixture",
    "health": "mock",
    "perf_summary": "live",
    "perf_open": "live"
  },
  "ts": "2026-05-18T..."
}
```

Sondage : interroge webhook_server:8000/api/state et /api/risk/status (timeout 2s, fallback graceful).

### Page Desk Pro mise à jour

Ajout d'une card "Pipeline Status" dans `/desk/ui` avec les infos clés.

## 13_ESTABLISHED

| Fait | Preuve |
|---|---|
| `GET /api/state` existe sur webhook_server:8000 | code ligne 621 |
| `GET /api/risk/status` existe sur webhook_server:8000 | code ligne 683 |
| `GET /desk/health` existe sur port 8010 | routes.py:28 |
| `GET /perf/summary` existe sur port 8010 | perf_app.py:405 |

## 16_TODO

1. Ajouter `GET /desk/status` à routes.py
2. Mettre à jour la page `/desk/ui` avec card pipeline status
3. Lancer Desk Pro + webhook + tester
4. Tester fallback quand webhook est down
5. unittest 92/92 PASS
