---
doc_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01_REPRISE
doc_type: reprise
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
mode: CONTROLLED_EXECUTION
source_kind: canonical
updated_at: 2026-05-28
---

# 90_REPRISE

## Point de reprise

1. Precheck read-only (git status/diff/untracked).
2. Inventaire metadata-only (.claude, artifacts/backtests).
3. Inventaire secrets (metadata global uniquement, pas de listing detaille si risque).
4. Creer la quarantine hors-repo.
5. Deplacer uniquement `.claude/` et `artifacts/backtests/`.
6. Post-check : `git status --short --branch` + `git ls-files --others --exclude-standard`.

Note : si `/opt/trading_runtime_quarantine/` n'est pas writable, utiliser un fallback hors-repo writable (ex: `/home/ghost/trading_runtime_quarantine/...`) sans sudo.

## Contraintes (rappel)

- Interdit : lecture/affichage contenu secrets.
- Interdit : deplacement/suppression secrets.
- Interdit : `git pull/reset/clean` sur db-layer.

## Close-gate parent

```text
PARENT_STATUS = CLOSEOUT_BLOCKED
RUNTIME_DEPLOY = NOT_PROVEN
```
