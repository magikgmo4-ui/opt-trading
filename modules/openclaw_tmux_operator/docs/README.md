# openclaw_tmux_operator

Module léger READ_ONLY pour OpenClaw : status/logs/health/attach hints tmux.

## Usage

```bash
# Statut fleet (dry-run, local)
bash modules/openclaw_tmux_operator/scripts/cmd.sh fleet-status

# Statut machine (SSH)
bash modules/openclaw_tmux_operator/scripts/cmd.sh machine-status db-layer
bash modules/openclaw_tmux_operator/scripts/cmd.sh tmux-status admin-trading

# Hint d'attachement
bash modules/openclaw_tmux_operator/scripts/cmd.sh attach-hint admin-trading desk-pro

# Logs — hint (path seulement)
bash modules/openclaw_tmux_operator/scripts/cmd.sh logs openclaw-core

# Logs — dernières lignes réelles
bash modules/openclaw_tmux_operator/scripts/cmd.sh session-logs openclaw-core 50
bash modules/openclaw_tmux_operator/scripts/cmd.sh session-logs fleet-status 100

# Health local (toutes sessions tmux)
bash modules/openclaw_tmux_operator/scripts/cmd.sh health-all

# Health aggregé multi-machines (SSH)
bash modules/openclaw_tmux_operator/scripts/cmd.sh health-aggregate
bash modules/openclaw_tmux_operator/scripts/cmd.sh health-aggregate --dry-run

# OpenClaw gateway (SSH vers db-layer)
bash modules/openclaw_tmux_operator/scripts/cmd.sh openclaw-health
bash modules/openclaw_tmux_operator/scripts/cmd.sh openclaw-health db-layer
bash modules/openclaw_tmux_operator/scripts/cmd.sh openclaw-probe db-layer
```

## health_aggregate.py — usage direct

```bash
# Toutes les machines Linux du map
python3 modules/openclaw_tmux_operator/scripts/health_aggregate.py

# Machines spécifiques
python3 modules/openclaw_tmux_operator/scripts/health_aggregate.py --machines db-layer,admin-trading

# Dry-run (pas de SSH — CI / local)
python3 modules/openclaw_tmux_operator/scripts/health_aggregate.py --dry-run
```

## Règles

- READ_ONLY : status, logs, health, hints uniquement
- Ne remplace pas `scripts/ai/workers/orchestration/` (PR #614)
- N'exécute pas de write externe
- Ne modifie pas les sessions tmux
- Pas de restart critique
- Pas de secret

## Dépendances

- `modules/runtime_health/fleet_orchestrator.py` pour fleet-status
- `scripts/tmux/health_check.py` pour health-all
- `modules/gateway_openclaw/scripts/cmd.sh` pour openclaw-health/probe
- `config/machine_runtime_map.yml` pour health-aggregate (liste machines)
- SSH aux machines cibles pour machine-status / tmux-status / health-aggregate / openclaw-*
