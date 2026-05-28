---
doc_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01_OPENING
doc_type: opening
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
mode: CONTROLLED_EXECUTION
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
---

# 00 — Opening: db-layer repo hygiene quarantine (CONTROLLED_EXECUTION)

## Base

- `sot/mainline@bc3f594b` (post-merge PR #895)
- Parent : `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`
- Etat parent : `CLOSEOUT_BLOCKED`
- `RUNTIME_DEPLOY = NOT_PROVEN`

## Decision humaine (scope execution)

- Autorise : inventaire + quarantaine de `/opt/trading/.claude/`
- Autorise : inventaire + quarantaine de `/opt/trading/artifacts/backtests/`
- Interdit : tout deplacement/suppression de `/opt/trading/secrets/`
- Interdit : `git pull/reset/clean` sur db-layer
- Interdit : affichage de contenu des secrets

## Objectif

Retirer du repo `/opt/trading` les untracked non essentiels a l'execution runtime (tooling + artifacts), en les deplacant vers une quarantine hors-repo.

## Quarantine (hors-repo)

Racine recommandee :

`/opt/trading_runtime_quarantine/GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01/<timestamp>/`
