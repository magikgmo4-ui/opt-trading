---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_CLOSEOUT_LOT2B_LOT3_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_CLOSEOUT_LOT2B_LOT3_01
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: closed
opened_at: 2026-06-02
---

# GO_OPENCLAW_DBLAYER_WORKERS_CHILD_CLOSEOUT_LOT2B_LOT3_01

## 1_MASTER_TARGET

Triple livraison :
1. Closeout batch — fermer 18 GOs éligibles
2. Lot 2B — activer les 5 jobs différés (infra disponible en dry-run)
3. Lot 3 — activer 9 jobs HITL/cockpit/scheduler/security

## 2_CLOSEOUT BATCH (18 GOs)

`status: open` → `status: closed` dans 00_INITIAL_PROJECT_DOC.md :
- 5 DBLAYER_DOCS_RESEARCH_LIBRARY children (EXTRACTION, FILESCOPE, FLEET_MATRIX, LOOP_CONTRACT, STUDENT_LAB)
- 5 DBLAYER_WORKERS children (BRIDGE_DISPATCH, JOBS_ACTIVATION, LOT1_CRON, LOT1_SMOKE, STRICT_DISPATCHER)
- 4 DBLAYER_GATEWAY/ORCHESTRATOR children
- 4 STRICT_WORKERS children (E2E_PIPELINE, PATCH_APPLY, PATCH_DRAFT, RUNNER_WRITEGATED)

## 3_LOT 2B (5 scripts)

| script | job_id | cadence |
|---|---|---|
| `capability_matrix_validate.py` | capability-matrix-validate | nightly |
| `hitl_scenarios_smoke.py` | hitl-scenarios-smoke | nightly |
| `ai_team_handoff_dry_run.py` | ai-team-handoff-dry-run | nightly |
| `task_router_dry_run.py` | task-router-dry-run | nightly |
| `localcms_workers_state_sync.py` | localcms-workers-state-sync | 30 min |

## 4_LOT 3 (9 scripts)

| script | job_id | cadence |
|---|---|---|
| `external_token_presence_check.py` | external-token-presence-check | daily |
| `deny_by_default_check.py` | deny-by-default-check | daily |
| `approval_expiry_check.py` | approval-expiry-check | hourly |
| `pending_approvals_digest.py` | pending-approvals-digest | hourly |
| `ai_team_role_registry_check.py` | ai-team-role-registry-check | daily |
| `scheduler_crontab_list.py` | scheduler-user-timers-list | daily |
| `scheduler_dead_letter_check.py` | scheduler-dead-letter-check | hourly |
| `localcms_ledger_view_refresh.py` | localcms-ledger-view-refresh | 15 min |
| `localcms_safe_buttons_check.py` | localcms-safe-buttons-check | daily |
