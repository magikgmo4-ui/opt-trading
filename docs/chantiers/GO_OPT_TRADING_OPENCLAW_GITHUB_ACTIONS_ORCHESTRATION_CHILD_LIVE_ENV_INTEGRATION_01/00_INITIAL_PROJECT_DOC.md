---
go_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_LIVE_ENV_INTEGRATION_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
1_MASTER_TARGET: github_actions_openclaw
topic_keys:
  - opt-trading
  - github_actions
  - openclaw
  - live_integration
  - env
  - testing
links:
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_CLOSEOUT_REVIEW_01/
  - scripts/openclaw_gh_actions_orchestrate.py
  - scripts/openclaw_gh_actions_route_job.py
  - scripts/openclaw_gh_actions_route_result.py
  - scripts/openclaw_gh_actions_analyze_failure_logs.py
  - scripts/openclaw_gh_actions_draft_failure_patch.py
  - scripts/openclaw_gh_actions_analyze_failure_logs_fix.py
---

# GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_LIVE_ENV_INTEGRATION_01

## Objet
Integrer les variables d'environnement (`GITHUB_TOKEN`, `GITHUB_REPOSITORY`) dans la chaine d'orchestration OpenClaw GitHub Actions : validation centralisee, test unitaire avec mocks des API calls, et utilite de dry-run E2E.

## Contexte
Le closeout review a identifie comme gap prioritaire le fait que les modes `--run-id` et `--analysis` dependent d'un environnement GitHub live, sans preuve E2E reelle capturee en CI.

Les scripts existants ont des live API paths qui doivent etre testables sans modifier les workflows ni introduire de mutation dangereuse.

## Perimetre
- creation de `scripts/openclaw_gh_actions_live_env.py` pour la validation env et le pipeline live
- couverture mockee des live API paths dans `tests/openclaw/test_openclaw_gh_actions_live_integration.py`
- aucune modification des workflows GitHub Actions

## Livrables attendus
- [x] `scripts/openclaw_gh_actions_live_env.py`
- [x] `tests/openclaw/test_openclaw_gh_actions_live_integration.py`
- [x] `20_ACCEPTANCE_REVIEW.md`
- [x] inbox entry

## 12_INVARIANTS
- No modification of global indexes.
- No modification of CI workflows.
- No modification of trading/runtime modules.
- No automatic mutations.
- `dangerous_action_executed: false`.

## 16_TODO
- [x] Initiation
- [x] Implementation
- [x] Validation mockee
- [ ] Manual live E2E proof
- [ ] Close Gate
