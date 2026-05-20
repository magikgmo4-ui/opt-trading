---
doc_id: GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01
status: active
source_kind: canonical
updated_at: 2026-05-20
---

# 00_INITIAL_PROJECT_DOC - mobile tmux operator smoke

## Stratégie

Les tests mobile réels (SSH depuis Termius/Termux vers db-layer) nécessitent un device Android physique — non testable en CI. Ce GO crée :

1. **Smoke tests CI** — valident la logique sans SSH réel ni device
2. **Script simulation** — reproduit le comportement mobile en local
3. **Checklist humaine** — matrice de validation à exécuter sur device réel

## État initial (après audit)

| Zone | Statut |
|---|---|
| `docs/chantiers/.../40_MOBILE_OPERATOR_ACCESS.md` (parent) | ✅ Runbook mobile complet |
| `modules/openclaw_tmux_operator/scripts/cmd.sh` (`attach-hint`) | ✅ Commande mobile clé |
| `modules/openclaw_tmux_operator/scripts/health_aggregate.py` | ✅ Dry-run utilisable depuis mobile |
| `scripts/tmux/mobile_smoke.sh` | present |
| `tests/mobile/test_mobile_smoke.py` | present |
| `docs/chantiers/.../10_HUMAN_CHECKLIST.md` | present |

## Machines cibles mobile

| Machine | Sessions prioritaires |
|---|---|
| db-layer | openclaw-core, fleet-status |
| admin-trading | desk-pro, screeners |

## MASTER_TARGET

Ce child reste subordonne au parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` via le GO
runtime `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`.

## Regle Kanban / continuite

Le tableau Kanban du bundle reste la navigation principale. Ce child documente
un sous-lot mobile, mais l'item Kanban exact reste le GO runtime tant que les
validations distantes ne sont pas executees.

## Prochain item Kanban exact

`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## Gaps encore ouverts

- validation Android device reel (Termius/Termux) encore PENDING
- commandes `bash` du module `openclaw_tmux_operator/scripts/cmd.sh` non
  executables dans ce workspace Windows sans WSL Linux
