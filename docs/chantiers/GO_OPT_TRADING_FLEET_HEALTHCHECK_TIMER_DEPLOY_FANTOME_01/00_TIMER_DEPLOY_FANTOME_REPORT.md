---
go_id: GO_OPT_TRADING_FLEET_HEALTHCHECK_TIMER_DEPLOY_FANTOME_01
doc_type: timer_deploy_report
status: CLOSED / MERGED
closed_at: 2026-05-19
---

# GO_OPT_TRADING_FLEET_HEALTHCHECK_TIMER_DEPLOY_FANTOME_01

## 1_MASTER_TARGET

Déployer le timer healthcheck sur `fantome` et le rendre visible dans `fleet_status.json`.
Avant ce GO : fantome était `unreachable`. Après : `reachable: true`, timer `PASS`.

---

## 7_CANONICAL_STATE

```text
TIMER_DEPLOY_FANTOME = CLOSED / MERGED
FANTOME_REACHABLE = true
FANTOME_SYSTEMD_TIMERS = PASS
FANTOME_MACHINE_IDENTITY = PASS
FANTOME_SOURCE = ssh (journald)
FLEET_ORCHESTRATOR_TIMER = active (waiting), every 5 min
UNITTEST = 111/111 PASS
SECRETS = NOT_INCLUDED
```

## Livrable

`deploy/systemd/overrides/fantome/opt-trading-runtime-health.service.d_override.conf`

```ini
[Service]
User=fantome
Group=fantome
```

## Validation post-merge

### Fleet orchestrator (db-layer)

```
opt-trading-fleet-orchestrator.timer
  Active: active (waiting) — every 5 min
  Next trigger: ~4min
```

### Fantome — timer système

```bash
systemctl list-timers --all | grep trading
# opt-trading-runtime-health.timer — last ran 49s ago, next in 4min 10s
```

| Check | Résultat |
|---|---|
| SSH fantome accessible | PASS — `hostname` retourne `fantome` |
| `opt-trading-runtime-health.timer` | PASS — système, pas `--user` |
| Service last run | `status=0/SUCCESS`, `elapsed=0.071s` |
| JSON produit (journald) | MACHINE_IDENTITY:PASS, SYSTEMD_TIMERS:PASS, VENV:PASS |
| `~/.local/share/.../latest.json` | ABSENT — output via journald uniquement |

### Fleet status post-collect

```json
{
  "fantome": {
    "reachable": true,
    "status": "WARN",
    "source": "ssh",
    "age_minutes": 1.8,
    "block_statuses": {
      "MACHINE_IDENTITY": "PASS",
      "SYSTEMD_TIMERS": "PASS",
      "FORBIDDEN_SERVICES": "PASS",
      "VENV": "PASS",
      ...
    }
  }
}
```

---

## 13_ESTABLISHED

- `fantome` passe de `unreachable` → `reachable: true` dans `fleet_status.json`.
- Timer `opt-trading-runtime-health.timer` actif au niveau système (non `--user`).
- Override `User=fantome Group=fantome` appliqué via drop-in systemd.
- Fleet orchestrator lit fantome via SSH + journald (`source: ssh`).
- `latest.json` non requis dans ce mode d'intégration.
- `cursor-ai` et `student` : inchangés (`unreachable` — hors scope).

---

## 15_REMAINING_GAP

| Gap | Impact |
|---|---|
| `SYSTEMD_SERVICES: WARN` (fantome) | Services attendus absents ou état non conforme — hors scope GO |
| `ENV/PORTS/HTTP/ARTIFACTS/LOGS: WARN` | Config fantome incomplète — à traiter en GO séparé |
| `cursor-ai`: unreachable | Hors scope GO |
| `student`: unreachable | Hors scope GO |
| `latest.json` absent | Fleet lit via journald — fonctionnel, pas bloquant |

---

## VERDICT

```text
PASS

fantome visible dans fleet_status.json    : PASS
fantome reachable                         : PASS (was unreachable)
SYSTEMD_TIMERS                            : PASS
MACHINE_IDENTITY                          : PASS
Fleet orchestrator timer (db-layer)       : active (every 5 min)
cursor-ai / student                       : inchangés (hors scope)
Tests 111/111                             : PASS
```
