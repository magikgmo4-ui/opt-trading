---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_YAML_FIX_01_INBOX
doc_type: inbox
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_YAML_FIX_01
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
status: open
created_at: 2026-05-25
---

# GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_YAML_FIX_01

Correction idiomatique du bloc YAML `run:` dans `gated-pr.yml`.

- **Cause** : le `:` dans `PASS:` casse le parsing YAML quand il est en valeur inline non protégée
- **Correctif** : remplacer `run: '...'` par `run: |\n  ...` (literal block scalar)
- **Prochaine étape** : `GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_TEST_01`
