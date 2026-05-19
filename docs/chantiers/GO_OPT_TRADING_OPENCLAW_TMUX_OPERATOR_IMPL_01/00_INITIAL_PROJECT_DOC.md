# GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01` |
| Objet | Enrichir `modules/openclaw_tmux_operator/` : health aggregator multi-machine, session-logs, intégration OpenClaw gateway |
| Parent | `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` (PR #618 MERGED) |
| Déclencheur | GAP-02 documenté dans 90_REPRISE.md du GO parent |
| Branche | `go/GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01` |

## État initial (après audit)

| Zone | Statut |
|---|---|
| `modules/openclaw_tmux_operator/scripts/cmd.sh` | ✅ Existe (6 commandes : fleet-status, machine-status, tmux-status, attach-hint, logs, health-all) |
| `modules/openclaw_tmux_operator/docs/README.md` | ✅ Existe (basique) |
| `modules/gateway_openclaw/scripts/cmd.sh` | ✅ Existe (health, probe, status, logs, attach) |
| `modules/runtime_health/fleet_orchestrator.py` | ✅ Existe (multi-machine, 456 lignes) |
| `scripts/tmux/health_check.py` | ✅ Existe (session health, 10 sessions) |
| `health_aggregate.py` dans openclaw_tmux_operator | ❌ Gap — à créer |
| `openclaw-health / openclaw-probe` dans cmd.sh | ❌ Gap — à ajouter |
| `session-logs` (vraies lignes) dans cmd.sh | ❌ Gap — à ajouter |
| Tests `tests/openclaw_tmux_operator/` | ❌ Gap — à créer |

## Scope

- READ_ONLY : aucune écriture session, aucun restart
- Aucun doublon avec `scripts/ai/workers/orchestration/` (PR #614)
- Aucune modification CI
- Aucune modification `tasks.index.json` / `models.registry.json`
