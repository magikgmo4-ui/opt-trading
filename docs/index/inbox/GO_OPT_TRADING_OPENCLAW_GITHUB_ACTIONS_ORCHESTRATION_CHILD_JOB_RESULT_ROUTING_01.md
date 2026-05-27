---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01_INBOX
doc_type: inbox
go_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
status: open
created_at: 2026-05-25
---

# GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01

Router le résultat d'un job GitHub Actions vers une décision contrôlée (PASS / FAIL / BLOCKED / NEEDS_HUMAN_REVIEW).

- **Script** : `scripts/openclaw_gh_actions_route_result.py`
- **Modes** : route (run_id réel ou simulé), list-classifications, test
- **Dépend sur** : PR #808 fusionnée, `scripts/openclaw_gh_actions_route_job.py` opérationnel
- **Prochaine étape** : `GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_FAILURE_LOGS_ANALYSIS_01`
