---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_BRANCH_CLEANUP_01_20_CLEANUP_ACTIONS
doc_type: chantier/cleanup_actions
repo: opt-trading
machine: cursor-ai
status: active
---

# 20_CLEANUP_ACTIONS

## Action 1 — Supprimer les branches locales stales

Commandes recommandees (a executer manuellement par l'operateur) :

```bash
# S'assurer d'etre sur sot/mainline ou une autre branche
git checkout sot/mainline

# Supprimer les 8 branches locales mergees
git branch -d go/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01
git branch -d go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
git branch -d go/GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01
git branch -d go/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01
git branch -d go/GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01
git branch -d go/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01
git branch -d go/GO_OPT_TRADING_CURSOR_AI_BUNDLES_MAINTENANCE_01
git branch -d go/GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01
```

Note : `git branch -d` (minuscule) ne supprime que si la branche est merged. Utiliser `-D` (majuscule) seulement si `-d` echoue avec une raison documentee.

## Action 2 — Verifier l'etat apres suppression

```bash
git branch | grep "CURSOR_AI"
# Attendu : seules les branches conservees + branche de travail
```

## Action 3 — Nettoyer les references remote stales

```bash
git remote prune origin
```

## Branches conservees

Ne pas supprimer :
- `go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_COWORK_LIVE_ARTIFACTS_REVIEW_01` — reference MACHINE_WORK_SPLIT
- `go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_PARENT_CLOSEOUT_01` — CLOSED (transport/docs)

## Note

Ce GO documente les actions de nettoyage. La suppression effective des branches locales est laissee a l'operateur (action manuelle, pas automatique).
