---
go_id: GO_OPT_TRADING_DESKPRO_RUNTIME_ALERT_DISPATCH_01
status: CLOSED
closeout_ts: 2026-05-18
---

## 13_ESTABLISHED

| Élément | État |
|---|---|
| PR `#552` | `MERGED` à `513c9f0c` |
| Branche feature | `go/GO_OPT_TRADING_DESKPRO_RUNTIME_ALERT_DISPATCH_01` supprimée |
| `sot/mainline` | mis à jour |
| Tests | `322/322 PASS` |
| `secrets/` | exclu |

## 7_CANONICAL_STATE

```text
DESKPRO_ALERT_DISPATCH = CLOSED / MERGED
PR_552 = MERGED
PIPELINE_ACTIONABLE_OBSERVABILITY = ACTIVE
ALERT_COOLDOWN = ACTIVE (300s, configurable via ALERT_COOLDOWN_SEC)
ALERT_PERSISTENCE = JSONL → /opt/trading/tmp/desk_pro_alerts.jsonl
DESK_ALERT_ENDPOINT = ACTIVE (/desk/alerts)
UI_ALERT_BAR = ACTIVE
UNITTEST = 322_PASS
NEXT = GO_OPT_TRADING_DESKPRO_ALERT_DESTINATIONS_01
```

## Livré

| Changement | Fichier |
|---|---|
| `_check_alert()` + `_read_alerts()` + `_alert_state` | `routes.py` |
| `ALERT_COOLDOWN_SEC` env configurable (default 300s) | `routes.py` |
| `ALERTS_JSONL` persistence | `routes.py` |
| `/desk/status` → champ `alert` | `routes.py` |
| `GET /desk/alerts` endpoint | `routes.py` |
| UI orange alert bar + muted cooldown info | `page.py` |

## Prochain GO

```text
GO_OPT_TRADING_DESKPRO_ALERT_DESTINATIONS_01
```

Objectif : brancher des destinations d'alerte optionnelles (Telegram, webhook) avec fallback JSONL/local.
