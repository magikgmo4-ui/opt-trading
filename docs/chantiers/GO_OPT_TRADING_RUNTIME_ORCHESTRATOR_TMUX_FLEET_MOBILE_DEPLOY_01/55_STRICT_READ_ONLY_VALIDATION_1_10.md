# 55 — Strict read-only validation (1 a 10)

## Objectif

Prouver, en mode strictement read-only, que le runtime operateur distant est accessible et coherent sur :

- `db-layer` (OpenClaw + fleet + tmux `openclaw-core`)
- `admin-trading` (tmux `desk-pro` et `screeners`)

Cette checklist ne declenche aucun deploy, aucun restart, aucune ecriture Google Sheets, et n'execute pas le watchdog.

## Prerequis

- poste operateur autorise (SSH fonctionnel vers `db-layer` et `admin-trading`)
- pas de modification locale : ne pas `git pull`, ne pas editer, ne pas lancer de scripts write

## Etapes 1 a 10 (ordre strict)

```bash
# 1. preflight repo db-layer
ssh db-layer 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'

# 2. preflight repo admin-trading
ssh admin-trading 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'

# 3. OpenClaw health (db-layer)
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health"'

# 4. OpenClaw probe (db-layer)
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh probe"'

# 5. fleet orchestrator dry-run (db-layer)
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'

# 6. tmux ls db-layer
ssh db-layer 'tmux ls'

# 7. tmux has-session openclaw-core (db-layer)
ssh db-layer 'tmux has-session -t openclaw-core'

# 8. tmux ls admin-trading
ssh admin-trading 'tmux ls'

# 9. tmux has-session desk-pro (admin-trading)
ssh admin-trading 'tmux has-session -t desk-pro || true'

# 10. tmux has-session screeners (admin-trading)
ssh admin-trading 'tmux has-session -t screeners || true'
```

## Stop conditions

- stop immediat si une des etapes 1 a 5 retourne `FAIL` ou `BLOCKED`
- ne pas lancer de smoke mobile reel tant que les etapes 1 a 10 ne sont pas stables

## Watchdog (11-12) optionnel

Les etapes watchdog ecrivent sous `/opt/trading/tmp/` (log + pid). Elles sont hors scope strict read-only.

## Gabarit de preuves a coller dans la reprise

| Etape | Host | Commande | Sortie utile | Verdict | Note / gap |
|---|---|---|---|---|---|
| 1 | `db-layer` | `test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch` | a renseigner | PENDING | |
| 2 | `admin-trading` | `test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch` | a renseigner | PENDING | |
| 3 | `db-layer` | `sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health"` | a renseigner | PENDING | |
| 4 | `db-layer` | `sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh probe"` | a renseigner | PENDING | |
| 5 | `db-layer` | `cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run` | a renseigner | PENDING | |
| 6 | `db-layer` | `tmux ls` | a renseigner | PENDING | |
| 7 | `db-layer` | `tmux has-session -t openclaw-core` | a renseigner | PENDING | |
| 8 | `admin-trading` | `tmux ls` | a renseigner | PENDING | |
| 9 | `admin-trading` | `tmux has-session -t desk-pro || true` | a renseigner | PENDING | |
| 10 | `admin-trading` | `tmux has-session -t screeners || true` | a renseigner | PENDING | |

Verdicts autorises : `PASS`, `WARN`, `FAIL`, `BLOCKED`.
