# 50 — Plan d'implémentation

## Cadre de cette passe

Cette passe reste bornee a la documentation, a la verification repo-first et a
des validations locales non destructives. Les commandes SSH ci-dessous sont le
plan cible a executer depuis le bon reseau operateur, pas des commandes
considerees comme deja passees ici.

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

Critere cible : user=`openclaw`, host=`db-layer`, `health` OK, `probe` OK.

## Phase C — Fleet orchestrator dry-run

```bash
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --no-telegram'
```

Critere cible : `unreachable=[]`, `failing=[]`, WARN seulement `EXPECTED`.

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
`scripts/tmux/sessions/fleet-status.sh` existe deja dans le repo ; il reste a
verifier sa presence en session distante via SSH.

## Phase E — Etendre `modules/openclaw_tmux_operator/` si necessaire

Le module READ_ONLY existe deja avec :

```
modules/openclaw_tmux_operator/
  scripts/cmd.sh
  scripts/health_aggregate.py
  docs/README.md
```

Capacites prouvees dans le repo :

- `fleet-status`
- `machine-status`
- `tmux-status`
- `attach-hint`
- `logs`
- `session-logs`
- `health-all`
- `health-aggregate`
- `openclaw-health`
- `openclaw-probe`

Role : status/logs/health/attach hints. Pas d'execution IA concurrente.

Extensions futures permises seulement si un gap reel apparait apres validation
distante ou smoke mobile.

## Phase F — Tests E2E

1. db-layer OpenClaw health
2. Fleet dry-run
3. tmux list db-layer
4. tmux list admin-trading
5. mobile attach/detach (simulation)
6. deskpro watchdog run-once
7. strict-workers readonly smoke
8. relecture reprise + gaps reels

## Phase G — Closeout

Maintenir `90_REPRISE.md` ouvert tant que :

- les validations distantes `db-layer` / `admin-trading` ne sont pas executees
- le smoke mobile reel n'est pas prouve
- le closeout umbrella final reste bloque par d'autres surfaces ouvertes
