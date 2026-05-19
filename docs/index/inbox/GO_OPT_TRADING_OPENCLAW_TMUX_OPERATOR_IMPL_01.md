# GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01

**État:** En cours
**Branche:** `go/GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01`
**Parent:** `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` (PR #618)

Enrichissement de `modules/openclaw_tmux_operator/` : health aggregator multi-machine, session-logs, intégration OpenClaw gateway.

## Livrables

- `modules/openclaw_tmux_operator/scripts/health_aggregate.py` — agrégateur Python multi-machines
- `modules/openclaw_tmux_operator/scripts/cmd.sh` — +4 commandes (health-aggregate, openclaw-health, openclaw-probe, session-logs)
- `modules/openclaw_tmux_operator/docs/README.md` — mis à jour
- `tests/openclaw_tmux_operator/test_health_aggregate.py` — 35 tests

## Dépendances

- PR #614 : squelette non modifié
- `modules/runtime_health/fleet_orchestrator.py` : réutilisé
- `modules/gateway_openclaw/scripts/cmd.sh` : cible openclaw-health/probe
- `config/machine_runtime_map.yml` : source machines

## NEXT_GO

- `GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01`
