---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_01_INBOX
doc_type: inbox
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_01
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
status: open
created_at: 2026-05-25
---

# GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_01

Correction de l'activation/parsing GitHub Actions de `gated-pr.yml`.

- **Chantier** : `docs/chantiers/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_01/`
- **Cause** : `merge_group` sans `types: [checks_requested]` invalide + `workflow_dispatch` sans input explicite
- **Correctif** : `merge_group.types: [checks_requested]` + `workflow_dispatch.inputs.reason`
- **Jobs conservés** : `gate/preflight`, `gate/file-scope`, `gate/no-lock-overlap`, `gate/tests`
- **Prochaine étape** : `GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01`
