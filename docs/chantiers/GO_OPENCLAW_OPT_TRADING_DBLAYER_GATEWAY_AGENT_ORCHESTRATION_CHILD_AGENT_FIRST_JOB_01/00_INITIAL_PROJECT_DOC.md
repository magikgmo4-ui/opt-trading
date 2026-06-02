---
doc_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_CHILD_AGENT_FIRST_JOB_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_CHILD_AGENT_FIRST_JOB_01
parent_go: GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_PARENT_01
status: closed
lifecycle_stage: cadrage
created_at: 2026-05-31
machine: db-layer
---

# 00_INITIAL_PROJECT_DOC — Child : Premier Job via Agent OpenClaw FORMAT 1→5

## 1_MASTER_TARGET

Prouver le premier job orchestrateur complet via le layer agent OpenClaw :
FORMAT 1 job spec → `openclaw agent --agent orchestrateur` → dispatch
`desk_pro_orchestrator` PAPER → FORMAT 3 résultat → FORMAT 4 synthèse
→ FORMAT 5 gate humain APPROVE.

## 2_PREREQUIS_RESOLU

```text
openclaw groupe ghost : ajouté (usermod -aG ghost openclaw)
Motif : /opt/trading/data/ est 775 ghost:ghost — openclaw avait besoin du groupe
gateway redémarré après usermod pour que la session hérite des groupes
```
