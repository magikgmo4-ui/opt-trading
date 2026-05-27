---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_ROUTING_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_github_actions
go_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_ROUTING_01
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
status: open
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_GITHUB_ACTIONS_OPENCLAW
MASTER_PROJECT_PLAN_ID: MPP_GITHUB_ACTIONS_OPENCLAW
PARENT_GO_ID: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
1_MASTER_TARGET: github_actions_openclaw
NEXT_GO: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01
topic_keys:
  - opt-trading
  - github_actions
  - openclaw
  - job_routing
links:
  - scripts/openclaw_gh_actions_route_job.py
---

# GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_ROUTING_01

## Objet

Passer de l'orchestration d'un job explicite à un routage contrôlé des jobs GitHub Actions avec validation multi-critères.

## Définition

OpenClaw doit pouvoir charger le registry, filtrer les jobs par job_id/role/risk_level/owner_surface/requires_secret/status, refuser les jobs invalides, sélectionner un job autorisé, déclencher workflow_dispatch, poller, classifier, et produire un rapport.

## Contraintes

- Pas d'auto-merge, apply patch, push vers sot/mainline
- Pas de trading runtime, secrets, contournement GitHub Actions
- Humain dans la boucle
