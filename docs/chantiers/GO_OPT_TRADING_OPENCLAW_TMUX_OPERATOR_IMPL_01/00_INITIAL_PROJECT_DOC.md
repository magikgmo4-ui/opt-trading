---
doc_id: GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01
status: active
source_kind: canonical
updated_at: 2026-05-20
---

# 00_INITIAL_PROJECT_DOC - openclaw tmux operator impl

## MASTER_TARGET

Ce child reste subordonne au parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` via le
sous-lot runtime `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`.

Il contribue a la surface runtime operateur distant du produit final total,
sans se substituer au closeout runtime ni au closeout umbrella.

## But

Documenter et verifier l'enrichissement READ_ONLY de
`modules/openclaw_tmux_operator/` :

- health aggregation multi-machines
- session logs read-only
- wrappers `openclaw-health` / `openclaw-probe`

## Etat actuel prouve dans le repo

| Zone | Statut |
|---|---|
| `modules/openclaw_tmux_operator/scripts/cmd.sh` | present |
| `modules/openclaw_tmux_operator/scripts/health_aggregate.py` | present |
| `modules/openclaw_tmux_operator/docs/README.md` | present |
| `tests/openclaw_tmux_operator/test_health_aggregate.py` | present |
| `modules/gateway_openclaw/scripts/cmd.sh` | present |
| `modules/runtime_health/fleet_orchestrator.py` | present |
| `scripts/tmux/health_check.py` | present |

## Invariants

- READ_ONLY : aucune ecriture session, aucun restart
- aucun doublon avec `scripts/ai/workers/orchestration/` (PR #614)
- aucune modification CI
- aucune modification `tasks.index.json` / `models.registry.json`

## Regle Kanban / continuite

Le tableau Kanban du bundle reste la carte de navigation principale. Ce child
documente un sous-lot runtime reel local, mais ne remplace pas le GO runtime
parent comme item Kanban exact tant que les validations distantes ne sont pas
prouvees.

## Prochain item Kanban exact

`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## Gaps encore ouverts

- validations SSH reelles de `openclaw-health` / `openclaw-probe` non executees
- `health-aggregate` reel hors `--dry-run` non execute depuis le bon reseau
- environnement Windows courant impropre aux commandes `bash` sans WSL Linux
