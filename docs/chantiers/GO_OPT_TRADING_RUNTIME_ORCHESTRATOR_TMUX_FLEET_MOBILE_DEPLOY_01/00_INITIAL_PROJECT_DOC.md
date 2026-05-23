---
doc_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: active
source_kind: canonical
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/20_MACHINE_TMUX_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/50_IMPLEMENTATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/55_STRICT_READ_ONLY_VALIDATION_1_10.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/56_STRICT_READ_ONLY_VALIDATION_RESULTS_1_10.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/60_TEST_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/70_USAGE_RUNBOOK.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/90_REPRISE.md
---

# 00_INITIAL_PROJECT_DOC - runtime orchestrator tmux fleet mobile

## MASTER_TARGET

Ce child contribue au produit final total du parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01`, avec
separation stricte entre :

- runtime operateur distant
- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Telegram screener inbound
- Telegram notification outbound multi-destinations
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## But

Documenter et verifier la surface runtime operateur distant reellement presente
dans le repo :

- orchestration OpenClaw sur `db-layer`
- fleet health via `modules/runtime_health/fleet_orchestrator.py`
- sessions tmux cote `db-layer` et `admin-trading`
- acces operateur mobile via SSH + tmux server-side

Ce cadrage reste doc-first et repo-first. Il ne lance aucun runtime depuis cet
environnement.

## Etat actuel prouve dans le repo

| Zone | Statut |
|---|---|
| `modules/runtime_health/fleet_orchestrator.py` | present |
| `scripts/tmux/sessions/fleet-status.sh` | present |
| `scripts/tmux/sessions/openclaw-core.sh` | present |
| `scripts/tmux/sessions/screeners.sh` | present |
| `scripts/tmux/sessions/desk-pro.sh` | present |
| `scripts/tmux/health_check.py` | present avec `fleet-status` dans `ALL_SESSIONS` |
| `tests/tmux/test_health_check.py` | present |
| `modules/gateway_openclaw/scripts/cmd.sh` | present |
| `modules/openclaw_tmux_operator/` | present |
| docs chantier runtime | presentes |

## Machines cibles

| Machine | Role | Priorite |
|---|---|---|
| `db-layer` | OpenClaw main + donnees + fleet | P0 |
| `admin-trading` | runtime trading + Desk Pro | P0 |
| `fantome` | operateur secondaire | P2 |
| `student` | sandbox | P3 |
| `cursor-ai` | Windows IDE/patch/health | n/a |

## Invariants

- OpenClaw = orchestration ; OpenCode = execution
- PR #614 = squelette non-executant, a consommer sans le recreer
- mobile = terminal SSH/tmux, jamais runtime local
- `cursor-ai` = machine Windows, pas de tmux Linux force
- no secrets, no auto-trade, no destructive commandes

## Regle Kanban / continuite

Le tableau Kanban du bundle reste la carte de navigation principale. Ce child
documente la surface runtime operateur distant du produit final total et ne
remplace pas le bundle par une roadmap concurrente.

## Prochain item Kanban a boucler

`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## Gaps encore ouverts

- validations SSH/tmux distantes non executees depuis cet environnement
- smoke mobile physique non execute
- closeout umbrella final reste bloque tant que runtime/Bot Vision/collectors/Sheets globaux ne sont pas tous cadres
