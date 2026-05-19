---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_WATCHDOG_01
doc_type: watchdog_report
status: CLOSED / MERGED
closed_at: 2026-05-19
---

# GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_WATCHDOG_01

## 1_MASTER_TARGET

Transformer le monitoring passif en watchdog actif : poll périodique ports 8000/8010 + `/desk/health`, heartbeat journalisé, détection dégradation, alerte WARN/ALERT dans log.

---

## 7_CANONICAL_STATE

```text
WATCHDOG = CLOSED / MERGED
SCRIPT = scripts/deskpro_watchdog.sh
PID_FILE = tmp/deskpro_watchdog.pid
LOG_FILE = tmp/deskpro_watchdog.log
INTERVAL = WATCHDOG_INTERVAL env var (default 60s)
UNITTEST = 111/111 PASS
SECRETS = NOT_INCLUDED
```

## Livrable

`scripts/deskpro_watchdog.sh` — 5 subcommands :

| Commande | Comportement |
|---|---|
| `start` | Lance boucle de poll en background, écrit PID file |
| `stop` | SIGTERM + attente, supprime PID |
| `status` | PID + 3 dernières lignes du log |
| `run-once` | Un seul poll immédiat (utile pour cron/test) |
| `logs` | `tail -f` du watchdog log |

## Validation

### Services UP — poll nominal

```
[2026-05-19T07:20:17Z] HEARTBEAT port=8000 status=UP
[2026-05-19T07:20:17Z] HEARTBEAT port=8010 status=UP health=ok
[2026-05-19T07:20:25Z] STATUS health=down webhook:pass perf:pass webhook_activity:fail probe_errors:pass
```

### Service DOWN — détection dégradation

```
[2026-05-19T07:20:32Z] HEARTBEAT port=8000 status=UP
[2026-05-19T07:20:32Z] WARN port=8010 status=DOWN
[2026-05-19T07:20:32Z] STATUS health=unreachable
[2026-05-19T07:20:32Z] ALERT issues=1 — check services
```

### Daemon start/stop/status

| Étape | Résultat |
|---|---|
| `WATCHDOG_INTERVAL=5 start` | pid 62746, log démarré |
| `status` | RUNNING + 3 dernières lignes |
| `stop` | stopped, PID supprimé |

## 13_ESTABLISHED

- Watchdog détecte port DOWN en < 1s via `ss -ltnp`.
- `ALERT issues=N` émis si ≥ 1 port DOWN ou health FAIL.
- Heartbeat journal : chaque poll écrit `HEARTBEAT` (UP) ou `WARN` (DOWN) + `STATUS` health.
- `WATCHDOG_INTERVAL` configurable via env — défaut 60s.
- Aucun secret dans le log — uniquement ports, statuts, timestamps.
- Double start guard : no-op si déjà running.

## 15_REMAINING_GAP

| Gap | Impact |
|---|---|
| Pas d'auto-restart des services | Watchdog détecte et log, mais ne redémarre pas automatiquement — choix délibéré (sécurité) |
| `webhook_activity: fail` permanent | Dans `STATUS health=down` — attendu sans signal TradingView |
| Pas d'alerte externe du watchdog | Log uniquement — Telegram/webhook restent dans l'app FastAPI |

## VERDICT

```text
PASS

start/stop/status/run-once/logs : PASS
Détection DOWN (port 8010 absent) : PASS — WARN + ALERT émis
Heartbeat nominal (services UP)   : PASS
No secrets in log                 : PASS
Tests 111/111                     : PASS
```
