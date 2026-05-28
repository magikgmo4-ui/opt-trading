---
doc_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_01_REPRISE
doc_type: reprise
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
mode: PLAN_ONLY
source_kind: canonical
updated_at: 2026-05-28
---

# 90_REPRISE

## Point de reprise

Ce GO est PLAN_ONLY : aucun changement db-layer n'est autorise.

Actions a faire (documentation uniquement) :
- Relire `10_INVENTORY_PLAN.md` et `20_SAFE_QUARANTINE_PLAN.md`.
- Valider les commandes read-only d’inventaire (sans lecture du contenu des secrets).
- Valider le schema de classification et les actions candidates.

## Decision humaine requise (avant tout GO d’execution)

1. Ou mettre la quarantine (chemin hors repo) ?
2. Politique secrets :
   - backup obligatoire avant toute suppression
   - destination / rotation (si applicable)
3. Politique artifacts/backtests :
   - conserver ou purger apres backup
4. Politique `.claude/` :
   - conserver (rare) ou purge apres backup

## Next GO (candidat)

```text
SAFE_EXECUTION_GO_CANDIDATE = GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01
EXECUTION_ALLOWED (current GO) = NO
```

## Close-gate parent

```text
PARENT_STATUS = CLOSEOUT_BLOCKED
RUNTIME_DEPLOY = NOT_PROVEN
```
