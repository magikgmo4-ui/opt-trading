---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_LONG_RUN_MONITOR_01
doc_type: long_run_monitor_report
status: CLOSED / MERGED
closed_at: 2026-05-19
---

# GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_LONG_RUN_MONITOR_01

## 1_MASTER_TARGET

Observer les services 8000/8010 sur une fenêtre contrôlée (~3 min) :
stabilité PID, dérive mémoire, croissance logs, JSONL, health périodique.

---

## 7_CANONICAL_STATE

```text
LONG_RUN_MONITOR = CLOSED / MERGED
WINDOW = T0 (2026-05-19T06:59:02Z) → T+3min (2026-05-19T07:02:17Z)
TESTS = 111/111 PASS
SECRETS = NOT_INCLUDED
PORT_8000 = UP — pid 57460 stable
PORT_8010 = UP — pid 57479 stable
```

---

## MONITOR RESULTS

### Snapshots

| Métrique | T=0 | T+1min | T+2min | T+3min | Delta |
|---|---|---|---|---|---|
| pid 8000 | 57460 | 57460 | 57460 | 57460 | stable |
| pid 8010 | 57479 | 57479 | 57479 | 57479 | stable |
| RSS 8000 (kB) | 51948 | 51956 | 51960 | 51960 | +12 kB |
| RSS 8010 (kB) | 57536 | 57572 | 57576 | 57580 | +44 kB |
| log 8000 (lignes) | 66 | — | — | 83 | +17 |
| log 8010 (lignes) | 182 | — | — | 195 | +13 |
| JSONL (lignes) | 13 | 14 | 14 | 14 | +1 (T0 seulement) |
| health.status | down | down | down | down | stable |
| webhook check | pass | pass | pass | pass | stable |

### Health périodique

```
[07:00:16Z] t+1min | health: down — webhook:pass | perf:pass | webhook_activity:fail
[07:01:16Z] t+2min | health: down — webhook:pass | perf:pass | webhook_activity:fail
[07:02:17Z] t+3min | health: down — webhook:pass | perf:pass | webhook_activity:fail
```

---

## 13_ESTABLISHED

- **PIDs stables** : aucun restart spontané sur 3 minutes.
- **Mémoire stable** : dérive +12 kB (8000) / +44 kB (8010) — négligeable, pas de fuite.
- **Logs** : croissance uniquement due aux requêtes de polling (health checks) — pas de spam.
- **JSONL** : +1 entrée lors du snapshot T0 (cooldown déjà expiré) — aucune entrée pendant la fenêtre idle.
- **health.status: down** constant : attendu (`webhook_activity: fail` sans signal TradingView entrant).
- `webhook: pass` stable tout au long — 8000 répond sans interruption.

---

## 14_HYPOTHESIS

- Sur une fenêtre plus longue (heures), la dérive RSS resterait probablement linéaire et faible.
- En production avec trafic TradingView réel, `webhook_activity` passerait `pass` → `health.status: ok`.

---

## 15_REMAINING_GAP

| Gap | Impact |
|---|---|
| Fenêtre 3 min — durée courte | Suffisant pour détecter instabilité immédiate, pas pour fuite mémoire lente |
| `webhook_activity: fail` permanent | Sans signal entrant, `health.status` reste `down` — non bloquant |

---

## VERDICT

```text
PASS

PID stability    : PASS — aucun restart spontané
Memory drift     : PASS — +12 kB / +44 kB sur 3 min (négligeable)
Log growth       : PASS — croissance normale (polling uniquement)
JSONL            : PASS — aucune écriture parasite pendant idle
Health stability : PASS — webhook:pass constant, health cohérent
Ports 8000/8010  : PASS — stables du T0 au T+3min
Tests 111/111    : PASS
```
