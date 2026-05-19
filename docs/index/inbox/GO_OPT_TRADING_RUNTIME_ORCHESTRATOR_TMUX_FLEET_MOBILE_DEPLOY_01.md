# GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01

**État:** En cours
**Branche:** `go/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

Déploiement tmux multi-machines + accès mobile SSH/tmux, avec OpenClaw comme orchestrateur depuis db-layer.

## Docs chantier

- `00_INITIAL_PROJECT_DOC.md` — Cadrage et état initial
- `10_RECENT_PR_CROSS_REVIEW.md` — Analyse PR #614 et autres PRs récentes
- `20_MACHINE_TMUX_MATRIX.md` — Matrice machines/sessions
- `30_OPENCLAW_ORCHESTRATION_BINDING.md` — Binding OpenClaw/tmux/fleet
- `40_MOBILE_OPERATOR_ACCESS.md` — Runbook mobile
- `50_IMPLEMENTATION_PLAN.md` — Plan d'implémentation
- `60_TEST_PLAN.md` — Plan de tests
- `70_USAGE_RUNBOOK.md` — Usage quotidien
- `80_SECURITY_AND_STOP_CONDITIONS.md` — Stop conditions
- `90_REPRISE.md` — Reprise et closeout

## Dépendances

- PR #614 : squelette non-exécutant external apps (consommé, non modifié)
- runtime_health/fleet_orchestrator : existant
- gateway_openclaw : existant
- scripts/tmux/ : existant

## NEXT_GO

- `GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01`
- `GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01`
