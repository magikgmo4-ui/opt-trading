# 40 — Usage Runbook

## Opérations quotidiennes

### Vérifier l'état de la flotte

```bash
cd /opt/trading

# Dry-run rapide (local, pas SSH)
bash modules/openclaw_tmux_operator/scripts/cmd.sh fleet-status

# Agrégation multi-machines (SSH)
bash modules/openclaw_tmux_operator/scripts/cmd.sh health-aggregate
```

### Vérifier OpenClaw sur db-layer

```bash
bash modules/openclaw_tmux_operator/scripts/cmd.sh openclaw-health
bash modules/openclaw_tmux_operator/scripts/cmd.sh openclaw-probe
```

### Voir les derniers logs d'une session

```bash
bash modules/openclaw_tmux_operator/scripts/cmd.sh session-logs openclaw-core 50
bash modules/openclaw_tmux_operator/scripts/cmd.sh session-logs fleet-status 100
bash modules/openclaw_tmux_operator/scripts/cmd.sh session-logs desk-pro 30
```

### S'attacher à une session (depuis mobile)

```bash
# Obtenir le hint
bash modules/openclaw_tmux_operator/scripts/cmd.sh attach-hint db-layer openclaw-core
# → ssh db-layer
# → tmux attach -t openclaw-core
```

### Vérifier les sessions tmux locales

```bash
bash modules/openclaw_tmux_operator/scripts/cmd.sh health-all
```

## Cas d'erreur

| Erreur | Cause probable | Action |
|---|---|---|
| `no log at ...` | Session jamais démarrée ou logs non écrits | Vérifier si session active |
| `ssh: connect to host ... port 22: Connection refused` | Machine hors ligne | Vérifier fleet-status |
| `openclaw health unavailable` | openclaw non démarré sur db-layer | Vérifier tmux session openclaw-core |
| `timeout` dans health-aggregate | SSH lent / machine hors ligne | Normal si machine WARN/FAIL |
