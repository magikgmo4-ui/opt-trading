---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_CLOSEOUT_01_REGISTRY_STATUS
doc_type: registry_status
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_CLOSEOUT_01
registry_version: v1.6
snapshot_at: 2026-05-29
---

# 20_REGISTRY_STATUS

État de `docs/registry/JOBS_REGISTRY.md` v1.6 après la livraison D1-D5.

---

## Évolution par version

| Version | Date | GO | Changement |
|---------|------|----|-----------|
| v1.0 | 2026-05-28 | SEMIAUTO_JOBS_REGISTRY_PILOT_02 | Création registre canonique |
| v1.1 | 2026-05-28 | JOBS_DEDUP_AUDIT (audit) | Baseline |
| v1.2 | 2026-05-28 | DRAFT_PACKETS_PROMOTION_01 (D1) | 4 packets promus/deprecated ; section 3 mise à jour |
| v1.3 | 2026-05-28 | ADD_TEST_SIGNAL_SCHEDULE_BATCH_01 (D2) | B04/B05 signal+schedule ; section 4 tests ajoutés |
| v1.4 | 2026-05-28 | OAUTH_AUDIT_ADD_TEST_01 (D3) | aw_oauth_audit add_test → keep |
| v1.5 | 2026-05-28 | CANDIDATE_WORKERS_SMOKE_PROMOTE_01 (D5) | 3 workers candidate → active ; B04/B05 CLOSED |
| v1.6 | 2026-05-29 | MODELS_REGISTRY_FORMALIZE_01 (D4) | ai_models_registry experimental → candidate |

---

## Statuts Section 4 — AI workers Python (post v1.6)

| job_id | statut | tests |
|--------|--------|-------|
| `aw_ledger_writer` | active | — |
| `aw_ledger_replay` | active | — |
| `aw_ledger_rotation` | active | — |
| `aw_ledger_schema` | active | — |
| `aw_ledger_trace` | active | — |
| `aw_ledger_blocked` | active | — |
| `aw_doc_ops_constraint` | active | — |
| `aw_doc_ops_create` | active | — |
| `aw_doc_ops_index` | active | — |
| `aw_strict_denied_scan` | active | — |
| `aw_strict_log_archive` | active | — |
| `aw_strict_output_schema` | active | — |
| `aw_signal_processor` | candidate | test_signal_workers.py |
| `aw_signal_stats` | candidate | test_signal_workers.py |
| `aw_health_status` | active | — |
| `aw_stuck_job` | active | — |
| `aw_permission_drift` | active | — |
| `aw_oauth_audit` | candidate | test_oauth_scope_audit.py |
| `aw_repo_frontmatter` | active | — |
| `aw_repo_link_check` | active | — |
| `aw_kill_switch` | active | — |
| `aw_localcms_sync` | **active** ← promu D5 | test_candidate_workers.py |
| `aw_openclaw_mobile` | **active** ← promu D5 | test_candidate_workers.py |
| `aw_runner_readonly` | active | — |

## Statuts Section 2 — Entry points (post v1.6)

| job_id | statut |
|--------|--------|
| `ai_run_task` | active |
| `ai_validate_job` | active |
| `ai_tasks_index` | active |
| `ai_models_registry` | **candidate** ← promu D4 |

## Statuts Section 7 — Scripts opérateurs racine (post v1.6)

| job_id | statut |
|--------|--------|
| `op_verify_all` | active |
| `op_smoke` | active |
| `op_diagnose` | active |
| `op_post_change` | active |
| `op_deploy_wrappers` | **active** ← promu D5 |
| `op_desk_pro_cmd` | active |

---

## Anomalies restantes

| anomalie_id | état |
|-------------|------|
| B01 | CLOSED (D1) |
| B02 | CLOSED (D1) |
| B03 | CLOSED (D1) |
| B04 | **CLOSED** (D2) |
| B05 | **CLOSED** (D2) |
| B06 | Open — scripts apply_desk_pro_*.sh legacy (lot dédié requis) |
