# 60 — Test plan

## Niveau 0 — Git et scope

```bash
git status --short --branch
git diff --check
git diff --name-only
```

PASS : branche attendue, pas de dirty tree hors scope, pas de secret.

## Niveau 1 — OpenClaw db-layer

```bash
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health"'
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh probe"'
```

PASS : health OK, probe OK.

## Niveau 2 — Fleet

```bash
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
```

PASS : unreachable=[], failing=[], WARN seulement EXPECTED.

## Niveau 3 — tmux db-layer

```bash
ssh db-layer 'tmux ls'
ssh db-layer 'tmux has-session -t openclaw-core'
ssh db-layer 'tmux list-windows -t openclaw-core'
```

PASS : session existe, fenêtres attendues visibles.

## Niveau 4 — tmux admin-trading

```bash
ssh admin-trading 'tmux ls'
ssh admin-trading 'tmux has-session -t screeners || true'
ssh admin-trading 'tmux has-session -t desk-pro || true'
```

PASS : sessions P0 présentes ou gaps documentés.

## Niveau 5 — Mobile

Depuis mobile (ou simulation) :

```bash
ssh db-layer
tmux attach -t openclaw-core
```

PASS : attach fonctionne, detach fonctionne, session survit à déconnexion.

## Niveau 6 — Desk Pro watchdog

```bash
ssh admin-trading 'cd /opt/trading && bash scripts/deskpro_watchdog.sh run-once'
ssh admin-trading 'cd /opt/trading && bash scripts/deskpro_watchdog.sh status'
```

PASS : no alert spam, status lisible.

## Niveau 7 — strict-workers readonly

```bash
cd /opt/trading
scripts/ai/workers/run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
```

PASS : validation passée, aucun write runtime, argument positionnel respecté.
