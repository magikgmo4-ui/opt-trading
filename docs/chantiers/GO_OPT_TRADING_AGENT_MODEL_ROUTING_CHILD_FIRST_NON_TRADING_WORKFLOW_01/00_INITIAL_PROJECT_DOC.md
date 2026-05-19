---
doc_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_CHILD_FIRST_NON_TRADING_WORKFLOW_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_CHILD_FIRST_NON_TRADING_WORKFLOW_01
parent_go_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_OPERATIONAL_ADOPTION_GATE_01
machine: fantome
status: in_progress
lifecycle_stage: execution
topic_keys:
  - agent_model_routing
  - child
  - first_non_trading_workflow
  - triage
source_kind: canonical
updated_at: 2026-05-14
---

# GO_OPT_TRADING_AGENT_MODEL_ROUTING_CHILD_FIRST_NON_TRADING_WORKFLOW_01

## 1_MASTER_TARGET

Premier workflow reel non-trading utilisant le routage multi-provider adopte.
Tache : triage/classification de 15 chantiers recents par domaine et risque.

## 2_SURFACE_SELECTION

Surface autorisee : **doc audit / triage** (read-only, format structure, risque faible)
Conforme adoption gate : OUI

## 3_TASK_CLASSIFICATION

| Critere | Valeur |
|---------|--------|
| Type | read-only, format structure |
| Risque | faible |
| Format attendu | structure (tableau) |
| Surface | doc audit / triage |
| Provider | 0.5B agent chain (read-only, format libre → structure) |
