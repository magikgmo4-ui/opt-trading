# GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` |
| Objet | Déployer la colonne vertébrale runtime tmux multi-machines, accessible depuis mobile, orchestrée par OpenClaw sur db-layer |
| Déclencheur | PR #614 mergée (squelette non-exécutant external apps) ; besoin d'une couche opératoire tmux/fleet/mobile |
| Source | Bundle déposé, audit anti-doublon, PR #614, runtime_health existant, scripts/tmux/ existants |
| Branche | `go/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` |

## État initial (après audit)

| Zone | Statut |
|---|---|
| `scripts/tmux/` (16 fichiers) | ✅ Existe (start/stop/health/9 sessions) |
| `modules/gateway_openclaw/` (11 fichiers) | ✅ Existe |
| `modules/runtime_health/fleet_orchestrator.py` | ✅ Existe (456 lignes) |
| `deploy/systemd/opt-trading-fleet-orchestrator.{service,timer}` | ✅ Existe déjà |
| `scripts/ai/workers/orchestration/` (PR #614) | ✅ Squelette intact, non modifié |
| `scripts/ai/workers/run_task.sh` | ✅ Existe |
| `scripts/ai/workers/job_packets/` (22 packets) | ✅ Existe |
| `scripts/deskpro_watchdog.sh` | ✅ Existe |
| `modules/openclaw_tmux_operator/` | ❌ Gap confirmé |
| Doc mobile SSH/tmux dédiée | ❌ Gap |
| Docs chantier ce GO | ❌ À créer |

## Machines cibles

| Machine | Rôle | Priorité |
|---|---|---|
| db-layer | OpenClaw MAIN + données + fleet | P0 |
| admin-trading | Runtime trading + Desk Pro | P0 |
| fantome | Opérateur secondaire | P2 |
| student | Sandbox | P3 |
| cursor-ai | Windows IDE/patch/health | n/a |

## Invariants

- OpenClaw = orchestration, OpenCode = exécution
- GitHub Actions = validation/smoke/sentinel
- PR #614 = squelette non-exécutant, non à recréer
- Mobile = terminal SSH/tmux, pas runtime
- cursor-ai = pas tmux Linux forcé
- No secrets, no auto-trade, no destructive commandes
