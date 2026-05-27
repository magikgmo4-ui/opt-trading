---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RUNTIME_REPLAY_01_RUNBOOK
doc_type: runbook
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RUNTIME_REPLAY_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
source_kind: canonical
updated_at: 2026-05-27
---

# 10 — Runbook (read-only) : prouver le fix PyYAML en runtime

## Host cible (attendu)

- `db-layer` (principal pour STEP 5 / fleet/runtime health)

## Preflight (read-only)

```bash
ssh db-layer 'hostname; whoami; pwd'
ssh db-layer 'cd /opt/trading && git status --short --branch'
ssh db-layer 'cd /opt/trading && git log -1 --oneline --decorate'
```

## Preuve "python + yaml" (read-only)

```bash
ssh db-layer 'set -e; /opt/trading/venv/bin/python3 -c "import sys; import yaml; print(sys.executable); print(yaml.__version__)"'
ssh db-layer 'set -e; /usr/bin/python3 -c "import sys; import yaml; print(sys.executable); print(yaml.__version__)"'
```

Notes :
- Si le venv echoue sur `import yaml` mais /usr/bin/python3 reussit, le wrapper doit choisir /usr/bin/python3.
- Si les deux reussissent, le wrapper choisira le venv (prioritaire).

## Preuve wrapper (read-only)

```bash
ssh db-layer 'cd /opt/trading && sed -n "1,120p" scripts/fleet_orchestrator.sh'
ssh db-layer 'cd /opt/trading && sed -n "1,120p" scripts/runtime_healthcheck.sh'
```

## Optionnel : replay STEP 5

Replay no-write (recommande) : executer les modules Python en `--dry-run` (pas d'ecriture).

```bash
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --map config/machine_runtime_map.yml --dry-run --no-telegram'
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/healthcheck.py --dry-run --no-telegram'
```

Replay via wrappers systemd : peut ecrire sous `/opt/trading/data/runtime_health` (mkdir, latest.json, fleet_status.json). Ne pas executer sans accord explicite "write allowed".

Si un mode `--dry-run` no-write existe, l'utiliser uniquement apres verification des options.
