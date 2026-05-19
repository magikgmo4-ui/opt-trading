---
go_id: GO_OPT_TRADING_DESKPRO_RUNTIME_OBSERVABILITY_HISTORY_01
status: CLOSED
closeout_ts: 2026-05-18T06:37:29Z
---

## 13_ESTABLISHED

| Élément | État |
|---|---|
| PR `#547` | `MERGED` à `afdf945f` |
| Branche feature | `go/GO_OPT_TRADING_DESKPRO_RUNTIME_OBSERVABILITY_HISTORY_01` supprimée |
| `sot/mainline` | mis à jour (`aba85f82`) |
| `GET /desk/status` | enrichi : `sources`, `error_count`, `recent_errors`, `perf_open`, `webhook_metrics` |
| `GET /desk/errors` | historique d'erreurs avec `limit` param |
| Pipeline Status card | badges vert/rouge Desk Pro / Webhook / Perf + sources + errors |
| Raw JSON | accessible dans `<details>` replié |
| Tests | `322/322 PASS` |
| Services | `webhook_server:8000`, `perf_app+desk_pro:8010` |
| `pytest` | non requis |
| `secrets/` | exclu |

## 7_CANONICAL_STATE

```text
DESKPRO_RUNTIME_OBSERVABILITY = CLOSED / FULL
PR_544 = MERGED (pipeline status endpoint + UI card)
PR_547 = MERGED (error tracking + source status + structured badges)
PIPELINE_STATUS = LIVE_IN_DESKPRO_UI
ERROR_HISTORY = ACTIVE (/desk/errors)
WEBHOOK_METRICS = ACTIVE
PERF_OPEN_VISIBLE = ACTIVE
UNITTEST = 322_PASS
DESKPRO_PORT = 8010
WEBHOOK_PORT = 8000
NEXT = GO_OPT_TRADING_DESKPRO_RUNTIME_ALERTING_AND_HEALTH_BADGES_01
```

## Fichiers modifiés (cumul PR #544 + #547)

| Fichier | Lignes |
|---|---|
| `modules/desk_pro/api/routes.py` | +80 / -1 |
| `modules/desk_pro/ui/page.py` | +96 / -5 |

## Prochain GO recommandé

```text
GO_OPT_TRADING_DESKPRO_RUNTIME_ALERTING_AND_HEALTH_BADGES_01
```

Objectif : passer de **voir l'état** à **être alerté/actionnable** :
- badge `healthy / degraded / down`
- seuils d'erreur configurables
- alerte si dernier webhook trop ancien
- alerte si perf events absents
- source mode fixture/mock/live/down signalé
- notification Telegram/webhook future
