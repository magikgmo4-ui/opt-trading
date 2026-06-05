---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_SUPERVISION_01
doc_type: closeout
repo: opt-trading
status: CLOSED / MERGED
closed_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_SUPERVISION_01 — CLOSEOUT

## 7_CANONICAL_STATE

```text
ALERT_RUNTIME_SUPERVISION = CLOSED / MERGED
CODE_CHANGES = NONE
UNITTEST = 111_PASS
SECRETS = NOT_INCLUDED
PORT_8000 = tv-webhook.service / tmux trading-pipeline (DOWN en local)
PORT_8010 = tv-perf.service / uvicorn modules.perf.app:app (DOWN en local)
```

## Livrable

`ALERT_RUNTIME_SUPERVISION_RUNBOOK.md` — 9 sections :

1. Architecture services (8000/8010, tmux, systemd)
2. Démarrage local (tmux, Option A venv / Option B system python)
3. Démarrage production (systemd)
4. Health checks (desk/health, desk/status, desk/alerts, diagnose.sh)
5. Alert smoke test (POST /desk/alert/test masqué)
6. Vérification env masquée
7. Logs (uvicorn, JSONL, webhook, perf)
8. Restart séquence complète + note cooldown reset
9. Commandes quotidiennes récapitulatives

## Findings audit

| Élément | Constat |
|---|---|
| Port 8000 | `webhook_server.py` — `modules/webhook/cmd.sh run` ou tmux `trading-pipeline` |
| Port 8010 | `modules.perf.app:app` — `scripts/desk_pro_ui_toolbox_final_cmd.sh restart` ou uvicorn direct |
| Production | `tv-webhook.service` + `tv-perf.service` systemd (admin-trading) |
| Local dev | tmux sessions `desk-pro` + `trading-pipeline` |
| Venv | absent en local, `system python3` (miniforge3 3.13.12) utilisé |
| `scripts/diagnose.sh` | script complet déjà existant — à utiliser en premier |
| Cooldown | process-local, reset au restart — documenté |

## RISKS

- À qualifier.
