---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_github_actions
go_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01
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
NEXT_GO: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_FAILURE_LOGS_ANALYSIS_01
topic_keys:
  - opt-trading
  - github_actions
  - openclaw
  - result_routing
links:
  - scripts/openclaw_gh_actions_route_result.py
  - scripts/openclaw_gh_actions_route_job.py
---

# GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01

## Objet

Router le résultat d'un job GitHub Actions orchestré par OpenClaw vers une décision opératoire contrôlée (PASS / FAIL / BLOCKED / NEEDS_HUMAN_REVIEW) sans exécution automatique.

## État établi

- PR #808 fusionnée — `scripts/openclaw_gh_actions_route_job.py` opérationnel
- OpenClaw sait sélectionner et dispatcher un job GitHub Actions
- `classify_conclusion` et `propose_next_action` existent dans `openclaw_gh_actions_orchestrate.py`
- Run réel `26419447778` (github-actions-job-registry-check) classifié PASS

## Définition

À partir d'un run GitHub Actions, produire une décision structurée :

| Facteur | Source |
|---|---|
| status | API GitHub — queued / in_progress / completed |
| conclusion | API GitHub — success / failure / cancelled / timed_out / action_required / neutral / skipped |
| run_id | API GitHub — identifiant unique du run |
| html_url | Lien GitHub Actions |
| job_id | Registry OpenClaw |
| workflow | Fichier workflow associé |
| classification | PASS / FAIL / BLOCKED / NEEDS_HUMAN_REVIEW |
| logs_access | Logs disponibles ou absents |
| probable_cause | Inféré depuis conclusion + status |
| next_action | Proposition non exécutée |

## Contraintes

- Pas d'auto-merge, apply patch, push vers sot/mainline
- Pas de trading runtime, secrets, admin-trading
- Pas de contournement GitHub Actions ni gate/*
- Humain dans la boucle obligatoire
- Ne modifier que les surfaces dans FILE_SCOPE

## Mapping conclusion → classification

| conclusion | classification |
|---|---|
| success | PASS |
| failure | FAIL |
| cancelled | BLOCKED |
| timed_out | BLOCKED |
| action_required | NEEDS_HUMAN_REVIEW |
| neutral | NEEDS_HUMAN_REVIEW |
| skipped | NEEDS_HUMAN_REVIEW |
| null + completed | NEEDS_HUMAN_REVIEW |
| null + in_progress | BLOCKED |
| unknown | NEEDS_HUMAN_REVIEW |

## next_action proposée (non exécutée)

| classification | next_action |
|---|---|
| PASS | ready_for_human_review |
| FAIL | inspect_logs_and_prepare_fix |
| BLOCKED | unblock_permissions_or_timeout |
| NEEDS_HUMAN_REVIEW | manual_review_required |
