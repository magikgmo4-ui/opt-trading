# openclaw_tmux_operator

Module léger READ_ONLY pour OpenClaw : status/logs/health/attach hints tmux.

## Usage

```bash
bash modules/openclaw_tmux_operator/scripts/cmd.sh fleet-status
bash modules/openclaw_tmux_operator/scripts/cmd.sh machine-status db-layer
bash modules/openclaw_tmux_operator/scripts/cmd.sh tmux-status admin-trading
bash modules/openclaw_tmux_operator/scripts/cmd.sh attach-hint admin-trading desk-pro
bash modules/openclaw_tmux_operator/scripts/cmd.sh logs openclaw-core
bash modules/openclaw_tmux_operator/scripts/cmd.sh health-all
```

## Règles

- READ_ONLY par défaut : status, logs, health, hints
- Ne remplace pas `scripts/ai/workers/orchestration/`
- N'exécute pas de write externe
- Ne modifie pas les sessions tmux
- Pas de restart critique
- Pas de secret

## Dépendances

- `runtime_health/fleet_orchestrator.py` pour fleet-status
- `scripts/tmux/health_check.py` pour health-all
- SSH aux machines cibles pour machine-status / tmux-status
