---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_02_INBOX
doc_type: inbox
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_02
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
status: open
created_at: 2026-05-25
---

# GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_02

Stabilisation de `gated-pr.yml` : suppression temporaire de `merge_group`.

- **Chantier** : `docs/chantiers/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_02/`
- **Cause** : le bloc `merge_group` reste incompatible — le parsing global du workflow est invalide (runs échouent en 0s, HTTP 422 sur `workflow_dispatch`)
- **Correctif** : retirer complètement `merge_group` pour valider d'abord `workflow_dispatch` manuel et `pull_request` checks
- **Jobs conservés** : `gate/preflight`, `gate/file-scope`, `gate/no-lock-overlap`, `gate/tests`
- **Prochaine étape** : `GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01`
- **Optionnel plus tard** : `GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_MERGE_GROUP_REINTRODUCTION_01`
