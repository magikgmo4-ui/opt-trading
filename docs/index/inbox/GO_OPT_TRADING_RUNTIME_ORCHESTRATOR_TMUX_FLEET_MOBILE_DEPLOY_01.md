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
- modules/openclaw_tmux_operator : existant

## Continuité umbrella

- `MASTER_TARGET` : parent `GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01`
- Kanban bundle : reste la navigation principale
- item Kanban exact en cours : `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`
- closeout final umbrella : bloque par surfaces ouvertes

## Constats de cette passe

- `scripts/tmux/sessions/fleet-status.sh` est bien present dans le repo
- `modules/openclaw_tmux_operator/` est bien present dans le repo
- la doc runtime est recalee pour ne plus pretendre un closeout PASS local sans validations distantes
- aucune commande runtime distante n'est lancee depuis cet environnement
- `tests\tmux\test_health_check.py` passe localement : `32 passed`
- `health_aggregate.py --dry-run --machines db-layer,admin-trading` passe localement
- `tests.mobile.test_mobile_smoke` passe localement : `OK` avec `skipped=12` si `bash` indisponible (WSL sans distribution)
- `bash scripts/tmux/sanity.sh` est bloque ici car WSL n'a pas de distribution installee

## Gaps encore ouverts

- validations SSH `db-layer` / `admin-trading` non executees
- smoke mobile reel non execute
- surfaces umbrella encore ouvertes hors runtime

## Prochaine passe preparee

- ordre exact borne : preflight -> OpenClaw -> fleet -> tmux -> watchdog -> mobile
- captures attendues explicites pour la reprise runtime
- criteres de stop distants precises avant toute validation mobile
- tableau de resultats distant pret a remplir (2 niveaux) :
  - strict read-only : etapes 1 a 10
  - watchdog optionnel : etapes 11/12 (ecrit sous `/opt/trading/tmp/`)
- bloc operateur compact copier-coller ajoute dans le runbook et la reprise

## NEXT_GO

- `GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01` (avant mobile)
- `GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01` (apres OpenClaw)
