# 30 — OpenClaw orchestration binding

## Responsabilités

```
OpenClaw = orchestration
OpenCode = exécution
GitHub Actions = validation/smoke/sentinel
App bridges = accès contrôlé
tmux = persistance opératoire
fleet_status = état de vérité runtime
```

## Flux status

```
OpenClaw
  -> lit data/runtime_health/fleet_status.json
  -> classe PASS/WARN/FAIL
  -> propose action
  -> jamais restart critique sans gate
```

## Flux tmux

```
OpenClaw
  -> ssh machine tmux ls
  -> compare sessions attendues (matrice 20_MACHINE_TMUX_MATRIX)
  -> affiche attach-hint
  -> ne tue pas de session sans instruction explicite
```

## Flux strict-workers

À ne pas redoubler. Utiliser `scripts/ai/workers/run_task.sh <packet.json>`.

## Command layer tmux

Module `modules/openclaw_tmux_operator/` present dans le repo a cette passe :

```
bash modules/openclaw_tmux_operator/scripts/cmd.sh fleet-status
bash modules/openclaw_tmux_operator/scripts/cmd.sh machine-status db-layer
bash modules/openclaw_tmux_operator/scripts/cmd.sh tmux-status admin-trading
bash modules/openclaw_tmux_operator/scripts/cmd.sh logs openclaw-core gateway
bash modules/openclaw_tmux_operator/scripts/cmd.sh attach-hint admin-trading desk-pro
```

## Modes

| Mode | Autorisé | Interdit |
|---|---|---|
| READ_ONLY | status, logs, health | restart, write |
| DRAFT_ONLY | rapport, plan, diff proposal | write réel |
| WRITE_GATED | action bornée | sans approval |

## Limites

- Ne pas recréer `scripts/ai/workers/orchestration/`
- Ne pas modifier PR #614 skeleton
- Ne pas implémenter l'adaptateur external apps ici (GO futur `OPENCLAW_ADAPTER_IMPL`)
- Les commandes SSH/tmux restent des preuves de surface locale tant qu'elles ne
  sont pas executees sur `db-layer` et `admin-trading`
