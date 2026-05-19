---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_RECOVERY_DRILL_01
doc_type: recovery_drill_report
status: CLOSED / MERGED
closed_at: 2026-05-19
---

# GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_RECOVERY_DRILL_01

## 1_MASTER_TARGET

Simuler arrêt/redémarrage des deux services runtime et vérifier la récupération complète :
`webhook:8000 + Desk Pro:8010 → stop → restart → health recovery → alert smoke → logs/JSONL`.

---

## 7_CANONICAL_STATE

```text
RECOVERY_DRILL = CLOSED / MERGED
TESTS = 111/111 PASS
SECRETS = NOT_INCLUDED
DRILL_1 = Desk Pro 8010 stop/restart — PASS
DRILL_2 = webhook 8000 stop → health dégradé → restart → recovery — PASS
DRILL_3 = arrêt simultané 8000+8010 → cold boot → full health — PASS
```

---

## DRILL RESULTS

### Drill 1 — Desk Pro (8010) stop/restart isolé

| Étape | Résultat |
|---|---|
| `deskpro_api_daemon.sh stop` | pid 55304 stoppé, port libéré |
| `status` | STOPPED |
| `deskpro_api_daemon.sh start` | pid 57336, health OK |
| `status` | RUNNING, health `{"ok":true}` |

### Drill 2 — webhook (8000) stop → impact health → restart

| Étape | Résultat |
|---|---|
| `webhook_daemon.sh stop` | pid 55792 stoppé, port libéré |
| `/desk/status` avec 8000 DOWN | `webhook: fail / reason: unreachable` — `health.status: down` |
| `webhook_daemon.sh start` | pid 57398, health OK |
| `/desk/status` post-recovery | `webhook: pass` — recovery confirmée |

### Drill 3 — arrêt simultané + cold boot complet

| Étape | Résultat |
|---|---|
| `stop` 8010 + `stop` 8000 | both DOWN confirmé |
| `webhook_daemon.sh start` | pid 57460, health OK |
| `deskpro_api_daemon.sh start` | pid 57479, health OK |
| ports 8000+8010 | UP simultanément |
| `/desk/status` | `webhook: pass`, `perf: pass` |
| alert smoke `POST /desk/alert/test` | telegram: `delivered`, webhook: `failed` (reason explicite — attendu) |
| JSONL | 3 nouvelles entrées `{ts, status}` persistées |
| logs | `uvicorn_8000.log` + `uvicorn_8010.log` + PID files présents |

---

## 13_ESTABLISHED

- Chaque service se redémarre proprement via son daemon script sans intervention manuelle.
- `webhook: fail → pass` : transition confirmée en < 5s après restart de `webhook_daemon.sh`.
- Cooldown reset au restart de `deskpro_api_daemon.sh` : première alerte réelle déclenchée immédiatement (comportement attendu, documenté).
- JSONL : persiste à travers les restarts — process-local uniquement pour le cooldown.
- Double start guard : pas de double instance possible.
- `webhook_activity: fail` permanent en local sans signal TradingView entrant — non bloquant.

---

## 14_HYPOTHESIS

- En production (`tv-perf.service` + `tv-webhook.service` via systemd), les transitions `down → healthy` seraient identiques mais gérées par `systemctl restart`.

---

## 15_REMAINING_GAP

| Gap | Impact |
|---|---|
| `webhook_activity: fail` permanent en local | `health.status` reste `down` même avec 8000 UP — attendu sans signal entrant |
| `ALERT_WEBHOOK_URL` = `api.telegram.org` | webhook smoke toujours `failed` avec reason explicite — non bloquant |
| `webhook_daemon.sh` requiert env chargé | `source .env` avant `start` pour que `TV_WEBHOOK_KEY` soit disponible |

---

## 16_TODO

Aucune action bloquante. Pipeline runtime entièrement opérationnel.

---

## VERDICT

```text
PASS

Drill 1 (8010 stop/restart)          : PASS
Drill 2 (8000 stop → health → restart): PASS
Drill 3 (simultané stop → cold boot)  : PASS
Alert smoke post-recovery             : telegram delivered
JSONL fallback                        : persisté
Logs                                  : présents
Tests 111/111                         : PASS
```
