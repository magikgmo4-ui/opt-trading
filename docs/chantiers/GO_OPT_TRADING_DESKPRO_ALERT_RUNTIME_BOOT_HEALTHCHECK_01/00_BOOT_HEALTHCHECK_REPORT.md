---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_BOOT_HEALTHCHECK_01
doc_type: boot_healthcheck_report
status: CLOSED / MERGED
closed_at: 2026-05-19
---

# GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_BOOT_HEALTHCHECK_01

## 1_MASTER_TARGET

Valider le démarrage complet du runtime Desk Pro alert depuis zéro : `webhook:8000 + Desk Pro:8010 + /desk/status + /desk/alert + /desk/ui + logs + restart + env masqué + JSONL`.

---

## 3_INITIAL_NEED

Confirmer que les services 8000/8010, les endpoints Desk Pro, les alertes et les logs restent opérationnels après boot/restart suite à la livraison de PR #575 (`deskpro_api_daemon.sh`).

---

## 7_CANONICAL_STATE

```text
PR_575 = MERGED (2026-05-19T04:56:34Z)
BRANCH = go/GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_BOOT_HEALTHCHECK_01
TESTS = 111/111 PASS (avant et après boot)
SECRETS = NOT_INCLUDED
PORT_8010 = UP (deskpro_api_daemon.sh)
PORT_8000 = DOWN — webhook_server.py présent, modules/webhook/cmd.sh ABSENT
DAEMON_SCRIPT = scripts/deskpro_api_daemon.sh (PR #575)
ALERT_ENV = TELEGRAM_BOT_TOKEN+TELEGRAM_CHAT_ID set, ALERT_WEBHOOK_URL=api.telegram.org (invalide)
```

---

## BOOT_RESULT

| Check | Résultat | Preuve |
|---|---|---|
| port 8000 | NOT_PROVED | webhook_server.py présent, modules/webhook/cmd.sh absent, pas de daemon script |
| port 8010 | PASS | `deskpro_api_daemon.sh start` → pid 55113, health OK |
| `/desk/status` | PASS | `{"health":{"status":"down",...},"desk_pro":{"ok":true}}` — down attendu (8000 absent) |
| `/desk/alerts` | PASS | `{"ok":true,"destinations":{"telegram":true,"webhook":true}}` |
| `/desk/ui` | PASS | HTML `<!doctype html>…<title>Desk Pro</title>` retourné |
| alert smoke | telegram: delivered / webhook: failed (reason explicite) | `POST /desk/alert/test` → `{"ok":true,"dispatch":[...]}` |
| logs | PASS | `tmp/uvicorn_8010.log` présent, `tmp/deskpro_api.pid` présent |
| JSONL fallback | PASS | `tmp/desk_pro_alerts.jsonl` — 3 entrées réelles `{ts,status}` |
| restart | PASS | `deskpro_api_daemon.sh restart` → stopped 55113 → started 55304 → health OK |
| env masqué | PASS | aucun secret dans réponses API, aucun token dans logs |

---

## 13_ESTABLISHED

- `scripts/deskpro_api_daemon.sh` est le seul script officiel pour port 8010.
- Restart contrôlé : stop (SIGTERM) + start (nohup uvicorn) → health OK en < 5s.
- `POST /desk/alert/test` : telegram `delivered`, webhook `failed` avec reason explicite (ALERT_WEBHOOK_URL pointe vers api.telegram.org — comportement attendu depuis PR #569).
- JSONL : 3 entrées persistées depuis sessions antérieures — reset cooldown confirmé au restart.
- `/desk/status health.status = "down"` attendu car port 8000 absent en local.
- Double start guard : `deskpro_api_daemon.sh start` sur processus running → "already running", no-op.
- `modules/webhook/cmd.sh` est absent — référencé dans la runbook mais non livré.

---

## 14_HYPOTHESIS

- Port 8000 (`webhook_server.py`) démarrable via `python3 webhook_server.py` ou via tmux session `trading-pipeline`, mais non prouvé dans ce GO (env requis : `TV_WEBHOOK_KEY`, etc.).
- Production : `tv-perf.service` (systemd) gère port 8010 — non accessible en sandbox.

---

## 15_REMAINING_GAP

| Gap | Détail |
|---|---|
| Port 8000 sans daemon | `webhook_server.py` présent mais `modules/webhook/cmd.sh` absent — pas de `start\|stop\|status` officiel |
| ALERT_WEBHOOK_URL invalide | Pointe vers `api.telegram.org` — webhook destination toujours `failed` |
| health.status = "down" permanent | Tant que port 8000 absent, `webhook: fail` → `status: down` → alert cooldown actif |
| Cooldown reset au restart | Process-local — documenté, comportement attendu |

---

## 16_TODO

Actions recommandées si suivi :
1. Créer `scripts/webhook_daemon.sh` (start|stop|status|restart|logs) pour port 8000 — symétrique à `deskpro_api_daemon.sh`.
2. Corriger `ALERT_WEBHOOK_URL` dans `.env` : utiliser un endpoint générique ou laisser vide.
3. Démarrer `webhook_server.py` en local pour passer `health.status` de `down` à `ok`.

---

## 17_RESUME_POINT

GO complété. Pipeline validé côté port 8010. Port 8000 est le seul gap actif.

---

## VERDICT

```text
PARTIAL

Port 8010 : PASS — boot, status, alert, UI, logs, restart tous validés.
Port 8000 : NOT_PROVED — webhook_server.py présent, pas de daemon script, env non chargé.
Tests : 111/111 PASS.
```

## RISKS

- À qualifier.
