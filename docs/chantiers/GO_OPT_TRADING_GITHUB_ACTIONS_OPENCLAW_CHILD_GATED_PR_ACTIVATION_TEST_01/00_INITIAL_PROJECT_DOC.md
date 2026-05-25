---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_TEST_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: github_actions
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_TEST_01
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
status: open
lifecycle_stage: test
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_GITHUB_ACTIONS_OPENCLAW
MASTER_PROJECT_PLAN_ID: MPP_GITHUB_ACTIONS_OPENCLAW
PARENT_GO_ID: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
1_MASTER_TARGET: github_actions_openclaw
NEXT_GO: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01
topic_keys:
  - opt-trading
  - github_actions
  - gated_pr
  - activation_test
links:
  - .github/workflows/gated-pr.yml
---

# GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_TEST_01

## Objet

Valider en conditions réelles que le workflow `gated-pr.yml` est actif, parsé correctement, déclenchable via `workflow_dispatch`, et reporte les checks `gate/*` sur une PR.

## Séquence de test

1. `gh workflow run gated-pr.yml --ref sot/mainline -f reason=manual`
2. `gh run list --workflow gated-pr.yml --limit 5`
3. Créer une micro-PR docs-only (ce chantier)
4. Vérifier les checks `gate/*` sur la PR

## Critères PASS

- `workflow_dispatch` reconnu (plus de HTTP 422)
- Run manuel ne finit plus en 0s "workflow file issue"
- Une PR vers `sot/mainline` déclenche les checks `gate/*`
- `gate/preflight` → PASS
- `gate/file-scope` → PASS
- `gate/no-lock-overlap` → PASS
- `gate/tests` → PASS
