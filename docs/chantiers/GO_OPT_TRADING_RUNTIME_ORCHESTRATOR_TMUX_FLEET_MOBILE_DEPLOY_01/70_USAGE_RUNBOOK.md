# 70 — Usage runbook quotidien

## Check rapide matin

```bash
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
ssh db-layer 'tmux ls'
ssh admin-trading 'tmux ls'
```

## Lire état fleet

```bash
ssh db-layer 'cd /opt/trading && jq . data/runtime_health/fleet_status.json'
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

```bash
bash modules/openclaw_tmux_operator/scripts/cmd.sh fleet-status
bash modules/openclaw_tmux_operator/scripts/cmd.sh machine-status db-layer
bash modules/openclaw_tmux_operator/scripts/cmd.sh tmux-status admin-trading
bash modules/openclaw_tmux_operator/scripts/cmd.sh attach-hint admin-trading desk-pro
```
