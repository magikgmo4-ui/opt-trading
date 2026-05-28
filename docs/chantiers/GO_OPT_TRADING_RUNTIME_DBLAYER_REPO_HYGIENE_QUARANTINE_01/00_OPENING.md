---
doc_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_01_OPENING
doc_type: opening
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
mode: PLAN_ONLY
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
---

# 00 — Opening: db-layer repo hygiene / quarantine (PLAN_ONLY)

## Base operationnelle

- `sot/mainline@071816ce`
- Parent : `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`
- Etat parent : `CLOSEOUT_BLOCKED`
- `RUNTIME_DEPLOY = NOT_PROVEN`

## Contexte etabli

- PR #881 mergée : audit drift db-layer archivé ; `db-layer:/opt/trading` = clean côté tracked.
- Fix PyYAML fleet_orchestrator present sur le worktree db-layer.
- Untracked sensibles restants sur db-layer :
  - `.claude/`
  - `artifacts/backtests/`
  - `secrets/`

## Objectif

Préparer une procédure sûre d’inventaire, classification et quarantaine des untracked sur `db-layer:/opt/trading` :

- sans exécution
- sans déplacement
- sans suppression
- avec critères de décision et rollback

## Contraintes strictes

- PLAN_ONLY : `EXECUTION_ALLOWED = NO`
- Ne pas modifier db-layer.
- Ne pas faire `git pull/reset/clean` sur db-layer.
- Ne pas modifier les index globaux.
- Ne pas fermer le parent.

## Livrables

- `10_INVENTORY_PLAN.md`
- `20_SAFE_QUARANTINE_PLAN.md`
- `90_REPRISE.md`
