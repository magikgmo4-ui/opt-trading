---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT2_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT2_01
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: closed
opened_at: 2026-06-02
---

# GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT2_01

## 1_MASTER_TARGET

Activer les 14 jobs Lot 2A en run réel et cron récurrent.
Écrire les 8 scripts manquants identifiés dans la matrice d'activation.

## 2_NOUVEAUX SCRIPTS

| script | job_id |
|---|---|
| `kill_switch_state_check.py` | kill-switch-state-check |
| `anti_leak_scan.py` | anti-leak-scan |
| `strict_worker_failure_report.py` | strict-worker-failure-report |
| `repo_go_index_audit.py` | repo-go-index-audit |
| `repo_closeout_eligibility_check.py` | repo-closeout-eligibility-check |
| `repo_orphan_files_audit.py` | repo-orphan-files-audit |
| `repo_changelog_digest.py` | repo-changelog-digest |
| `strict_worker_registry_check.py` | strict-worker-model-registry-check + task-index-check |
| `env_file_presence_check.sh` | env-file-presence-check |
| `gitignore_secrets_policy_check.sh` | gitignore-secrets-policy-check |
| `repo_branch_audit.sh` | repo-branch-audit |

## 3_SCRIPTS EXISTANTS UTILISÉS

- `ledger_trace_id_audit.py` (déjà dans codebase)
- `strict_worker_output_schema_check.py` (déjà dans codebase)
- `oauth_scope_audit.py` (déjà dans codebase)

## 4_LOT 2B DIFFÉRÉ

5 jobs nécessitent une infrastructure non encore deployée :
- `capability-matrix-validate` — matrix à formaliser
- `hitl-scenarios-smoke` — HITL infra incomplète
- `ai-team-handoff-dry-run` — role registry absent
- `task-router-dry-run` — router à implémenter
- `localcms-workers-state-sync` — cockpit infra
