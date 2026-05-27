---
go_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_LIVE_E2E_MANUAL_TEST_01
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
  - live_e2e
  - manual_test
  - hitl
links:
  - docs/chantiers/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01/
  - docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml
  - docs/registries/GITHUB_ACTIONS_WORKFLOWS_INVENTORY_01.yml
  - scripts/openclaw_gh_actions_dry_run.py
  - modules/openclaw_github_actions_bridge/app/bridge.py
---

# GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_LIVE_E2E_MANUAL_TEST_01

## Objet
Executer un test E2E live manuel controle de la chaine OpenClaw GitHub Actions avec `GITHUB_TOKEN` et `GITHUB_REPOSITORY`, afin de prouver `run-info` et `pipeline` sur un vrai run GitHub Actions.

## Contexte
La chaine GitHub Actions/OpenClaw est exploitable en mode controle, mais le master target `github_actions_openclaw` n'est pas fermable tant qu'une preuve live reelle n'est pas capturee.

Le but de ce child GO n'est pas d'ajouter des workflows ni d'appliquer des patchs, mais de produire une preuve d'execution reelle et documentee.

## Perimetre
- preparation d'un test manuel controle avec `GITHUB_TOKEN` et `GITHUB_REPOSITORY`
- execution d'un run GitHub Actions reel sur un workflow deja autorise
- validation des surfaces `run-info` et `pipeline`
- production de `LIVE_E2E_TEST_REPORT_01.md`

## Hors perimetre
- aucune modification des workflows GitHub Actions
- aucun apply/merge/patch automatique
- aucun push vers `sot/mainline`
- aucune mutation trading/runtime

## Preconditions
- les secrets `GITHUB_TOKEN` et `GITHUB_REPOSITORY` sont disponibles dans l'environnement de test
- un workflow `workflow_dispatch` non destructif est selectionne
- si les surfaces live-env precedentes ne sont pas presentes dans la branche de travail, elles doivent etre restaurees avant execution du test reel

## Livrables attendus
- [ ] `LIVE_E2E_TEST_REPORT_01.md`
- [ ] Etat du test reel documente
- [ ] Verdict PASS/BLOCKED/FAIL documente sans mutation dangereuse

## 12_INVARIANTS
- No workflow changes.
- No patch application.
- No push to `sot/mainline`.
- HITL mandatory for any sensitive follow-up.
- `dangerous_action_executed: false`.

## 16_TODO
- [x] Initiation
- [ ] Preparation environment
- [ ] Manual live execution
- [ ] Report publication
- [ ] Close Gate
