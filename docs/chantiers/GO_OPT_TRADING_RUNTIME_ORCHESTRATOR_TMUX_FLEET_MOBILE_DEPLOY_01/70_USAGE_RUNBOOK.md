# 70 — Usage runbook quotidien

## Check rapide matin

```bash
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
ssh db-layer 'tmux ls'
ssh admin-trading 'tmux ls'
```

## Checklist distante minimale

Executer dans cet ordre depuis un poste autorise :

```bash
ssh db-layer 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'
ssh admin-trading 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health"'
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh probe"'
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
ssh db-layer 'tmux ls'
ssh db-layer 'tmux has-session -t openclaw-core'
ssh admin-trading 'tmux ls'
ssh admin-trading 'tmux has-session -t desk-pro || true'
ssh admin-trading 'tmux has-session -t screeners || true'
ssh admin-trading 'cd /opt/trading && bash scripts/deskpro_watchdog.sh run-once'
ssh admin-trading 'cd /opt/trading && bash scripts/deskpro_watchdog.sh status'
```

Note : les etapes 11/12 ecrivent sous `/opt/trading/tmp/` (watchdog log + pid).
Si un protocole strictement sans ecriture est requis, utiliser le bloc
"strict read-only" ci-dessous.

Ne pas poursuivre vers mobile si un preflight, un `health`, un `probe` ou un
`fleet FAIL` echoue.

## Bloc strict read-only (1 a 10)

```bash
# 1
ssh db-layer 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'
# 2
ssh admin-trading 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'
# 3
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health"'
# 4
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh probe"'
# 5
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
# 6
ssh db-layer 'tmux ls'
# 7
ssh db-layer 'tmux has-session -t openclaw-core'
# 8
ssh admin-trading 'tmux ls'
# 9
ssh admin-trading 'tmux has-session -t desk-pro || true'
# 10
ssh admin-trading 'tmux has-session -t screeners || true'
```

## Bloc unique copier-coller operateur

Copier ce bloc depuis un poste autorise, executer les 12 commandes dans l'ordre,
puis remplir le tableau de resultats ci-dessous.

```bash
# 1
ssh db-layer 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'
# 2
ssh admin-trading 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'
# 3
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health"'
# 4
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh probe"'
# 5
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
# 6
ssh db-layer 'tmux ls'
# 7
ssh db-layer 'tmux has-session -t openclaw-core'
# 8
ssh admin-trading 'tmux ls'
# 9
ssh admin-trading 'tmux has-session -t desk-pro || true'
# 10
ssh admin-trading 'tmux has-session -t screeners || true'
# 11
ssh admin-trading 'cd /opt/trading && bash scripts/deskpro_watchdog.sh run-once'
# 12
ssh admin-trading 'cd /opt/trading && bash scripts/deskpro_watchdog.sh status'
```

## Lire état fleet

```bash
ssh db-layer 'cd /opt/trading && jq . data/runtime_health/fleet_status.json'
```

En local/dry-run operator :

```powershell
python modules\openclaw_tmux_operator\scripts\health_aggregate.py --dry-run --machines db-layer,admin-trading
```

## Attacher OpenClaw

```bash
ssh db-layer
tmux attach -t openclaw-core
```

## Attacher Desk Pro

```bash
ssh admin-trading
tmux attach -t desk-pro
```

## Captures a reporter

Reporter dans la reprise runtime :

- host + commande
- sortie courte utile
- verdict `PASS` / `WARN` / `FAIL` / `BLOCKED`
- gap cree si la commande n'est pas executable depuis le reseau courant

## Gabarit de resultats a remplir

Utiliser le tableau suivant pendant la prochaine passe distante :

| Etape | Host | Commande | Sortie utile | Verdict | Gap / note |
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
| 11 | `admin-trading` | `cd /opt/trading && bash scripts/deskpro_watchdog.sh run-once` | a renseigner | PENDING | |
| 12 | `admin-trading` | `cd /opt/trading && bash scripts/deskpro_watchdog.sh status` | a renseigner | PENDING | |

Mode strict read-only : executer 1 a 10 uniquement et ecrire `WATCHDOG_SKIPPED`
en note. Mode watchdog : executer 11/12 ensuite (ecrit sous `/opt/trading/tmp/`).

Verdicts autorises :

- `PASS`
- `WARN`
- `FAIL`
- `BLOCKED`

Regle :

- stop immediat si une ligne preflight / OpenClaw / fleet tombe en `FAIL` ou `BLOCKED`
- mobile hors tableau tant que les 12 lignes ci-dessus ne sont pas stabilisees

## Lire logs

```bash
ssh db-layer 'tail -n 120 /opt/trading/logs/tmux_health.log'
ssh admin-trading 'journalctl -u tv-webhook.service -n 80 --no-pager'
ssh admin-trading 'journalctl -u tv-perf.service -n 80 --no-pager'
```

## Déclencher un strict-worker read-only

```bash
cd /opt/trading
scripts/ai/workers/run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
```

## Règle d'intervention

| Situation | Action |
|---|---|
| Fleet PASS | Continuer |
| Fleet WARN EXPECTED | Continuer, noter |
| Fleet WARN unknown | Investiguer avant action |
| Fleet FAIL | Stopper actions runtime |
| Machine unreachable | Pas de déploiement |
| Dirty tree | Stopper runner |
| Secret demandé | BLOCKED |

## Utiliser openclaw_tmux_operator (si créé)

Le module existe deja dans le repo ; les commandes ci-dessous restent
read-only et doivent etre executees uniquement depuis une machine autorisee.

```bash
bash modules/openclaw_tmux_operator/scripts/cmd.sh fleet-status
bash modules/openclaw_tmux_operator/scripts/cmd.sh machine-status db-layer
bash modules/openclaw_tmux_operator/scripts/cmd.sh tmux-status admin-trading
bash modules/openclaw_tmux_operator/scripts/cmd.sh attach-hint admin-trading desk-pro
bash modules/openclaw_tmux_operator/scripts/cmd.sh session-logs fleet-status 100
bash modules/openclaw_tmux_operator/scripts/cmd.sh health-aggregate --dry-run
```
