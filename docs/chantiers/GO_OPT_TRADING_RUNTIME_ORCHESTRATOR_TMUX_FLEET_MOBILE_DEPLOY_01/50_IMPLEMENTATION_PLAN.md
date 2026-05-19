# 50 — Plan d'implémentation

## Vue système

```
Mobile / Desktop / IDE
  -> SSH
  -> tmux server-side
  -> OpenClaw sur db-layer
  -> OpenCode / strict-workers si besoin
  -> runtime_health + fleet_status
  -> admin-trading / db-layer / fantome / student / cursor-ai
```

## Phase A — Docs chantier + cross-review ✅ (ce fichier)

Créer la structure de chantier avec état initial après audit.

## Phase B — Valider OpenClaw db-layer

```bash
ssh db-layer 'sudo -iu openclaw bash -lc "whoami; hostname; pwd; openclaw --version"'
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health"'
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh probe"'
```

PASS : user=openclaw, host=db-layer, health OK, probe OK.

## Phase C — Fleet orchestrator dry-run

```bash
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --no-telegram'
```

PASS : unreachable=[], failing=[], WARN seulement EXPECTED.

## Phase D — Valider tmux sessions

### db-layer
```bash
ssh db-layer 'tmux ls'
ssh db-layer 'tmux has-session -t openclaw-core'
```

### admin-trading
```bash
ssh admin-trading 'tmux ls'
ssh admin-trading 'tmux has-session -t screeners || true'
ssh admin-trading 'tmux has-session -t desk-pro || true'
```

### Gap connu
Créer `scripts/tmux/sessions/fleet-status.sh` si non existant.

## Phase E — Créer modules/openclaw_tmux_operator/

Module léger READ_ONLY :

```
modules/openclaw_tmux_operator/
  scripts/cmd.sh
  scripts/fleet_status.sh
  scripts/machine_status.sh
  scripts/tmux_status.sh
  scripts/tmux_attach_hint.sh
  scripts/session_logs.sh
  scripts/health_all.sh
  docs/README.md
```

Rôle : status/logs/health/attach hints. Pas d'exécution IA concurrente.

## Phase F — Tests E2E

1. db-layer OpenClaw health
2. Fleet dry-run
3. tmux list db-layer
4. tmux list admin-trading
5. mobile attach/detach (simulation)
6. deskpro watchdog run-once
7. strict-workers readonly smoke
8. Closeout

## Phase G — Closeout

Créer `90_REPRISE.md` avec :
- Commandes exécutées et résultats
- Gaps documentés
- NEXT_GO proposés
