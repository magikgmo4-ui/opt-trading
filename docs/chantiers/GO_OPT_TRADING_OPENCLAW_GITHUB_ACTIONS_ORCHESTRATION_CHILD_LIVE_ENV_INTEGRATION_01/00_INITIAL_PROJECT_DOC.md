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
Intégrer les variables d'environnement (GITHUB_TOKEN, GITHUB_REPOSITORY) dans la chaîne d'orchestration OpenClaw GitHub Actions : validation centralisée, test unitaire avec mocks des API calls, et utilité de dry-run E2E.

## Contexte
Le closeout review a identifié comme gap #1 : "Live API integration: --run-id and --analysis modes need GITHUB_TOKEN + GITHUB_REPOSITORY env. No end-to-end test against real GitHub Actions runs in CI."

Les scripts existants ont des live API paths qui ne sont pas testés unitairement. Les modifications directes sont bloquées (no-lock-overlap sur scripts/ existants claim par des GOs mergés).

## Périmètre
- Création de `scripts/openclaw_gh_actions_live_env.py` — utilitaire central de validation et d'orchestration live
- Création de `tests/openclaw/test_openclaw_gh_actions_live_integration.py` — tests mockés pour tous les live API paths
- Aucune modification des scripts existants (contournement no-lock-overlap)

## Livrables attendus
- [ ] `scripts/openclaw_gh_actions_live_env.py` — validation env, dry-run API, pipeline E2E
- [ ] `tests/openclaw/test_openclaw_gh_actions_live_integration.py` — mock tests
- [ ] `20_ACCEPTANCE_REVIEW.md`
- [ ] Inbox entry

## 12_INVARIANTS
- No modification of global indexes.
- No modification of CI workflows.
- No modification of trading/runtime modules.
- No modification of existing scripts in scripts/ (no-lock-overlap).
- No automatic mutations — `dangerous_action_executed: false`.

## 16_TODO
- [x] Initiation
- [ ] Implementation
- [ ] Validation
- [ ] Close Gate
