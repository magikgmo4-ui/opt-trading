---
doc_id: JOBS_REGISTRY_V1
doc_type: jobs_registry
repo: opt-trading
project: opt-trading
module: automation_ops
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_REGISTRY_01
status: open
version: v1
updated_at: 2026-05-28
source_kind: canonical
links:
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01/20_JOBS_REGISTRY_SPEC.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01/10_ARCHITECTURE_SURFACES.md
---

# JOBS_REGISTRY — v1

Registre canonique des jobs `opt-trading`.  
Schéma : `20_JOBS_REGISTRY_SPEC.md`.

Légende statuts :
- `active` — en production, consommé prouvé
- `candidate` — opérationnel, pas encore prouvé en production
- `experimental` — test / prototype / draft
- `deprecated` — remplacé, à supprimer
- `blocked` — consommateur ou permissions inconnus

---

## Section 1 — GitHub Actions workflows (7)

| job_id | path | type | trigger | owner_surface | outputs | permissions | status | tests | risk | next_action |
|---|---|---|---|---|---|---|---|---|---|---|
| `gha_gated_pr` | `.github/workflows/gated-pr.yml` | gha | pr / manual | CI/CD | CI status checks | aucun secret | active | tests/governance/ | medium | keep |
| `gha_registry_validation` | `.github/workflows/gh-actions-registry-validation.yml` | gha | pr (paths) / manual | CI/CD | rapport validation YAML | aucun secret | active | scripts/validate_gh_actions_registries.py | low | keep |
| `gha_openclaw_mcp_policy` | `.github/workflows/openclaw-mcp-policy-static-validator.yml` | gha | pr (paths) / manual | openclaw | rapport policy MCP | aucun secret | active | tests/test_openclaw_mcp_policy_validator.py | medium | keep |
| `gha_openclaw_skill_policy` | `.github/workflows/openclaw-skill-policy-warning-only.yml` | gha | manual only | openclaw | warning report | aucun secret | candidate | — | low | keep |
| `gha_strict_workers_schedule` | `.github/workflows/strict-workers-schedule.yml` | gha | schedule (lun 08:00) / manual | ai_workers | audit report | aucun secret | active | tests/test_signal_workers.py | medium | keep |
| `gha_strict_workers_smoke` | `.github/workflows/strict-workers-smoke.yml` | gha | pr (paths) / manual | ai_workers | smoke results | aucun secret | active | — | low | keep |
| `gha_strict_workers_validate` | `.github/workflows/strict-workers-validate.yml` | gha | pr (paths) / manual | ai_workers | validation job_packets | aucun secret | active | scripts/ai/workers/_validate_job.py | medium | keep |

---

## Section 2 — AI workers — entry point

| job_id | path | type | trigger | owner_surface | inputs | outputs | status | tests | risk | next_action |
|---|---|---|---|---|---|---|---|---|---|---|
| `ai_run_task` | `scripts/ai/workers/run_task.sh` | shell | manual / openclaw_call | ai_workers | job_packet JSON | worker output | active | strict-workers-smoke.yml | medium | keep |
| `ai_validate_job` | `scripts/ai/workers/_validate_job.py` | python | pr / manual | ai_workers | job_packets/*.json | validation report | active | strict-workers-validate.yml | low | keep |
| `ai_tasks_index` | `scripts/ai/workers/tasks.index.json` | config | — | ai_workers | — | constraints + task routing (denied_inputs:9, denied_commands:8, task_types:10) | active | strict-workers-validate.yml | medium | keep |
| `ai_models_registry` | `scripts/ai/workers/models.registry.json` | config | — | ai_workers | — | model routing | experimental | — | low | formalize |

---

## Section 3 — AI workers — job_packets (30)

Agrégat par statut et task_type :

| Statut packet | Count | Signification |
|---|---|---|
| `DRAFT_ONLY` | 22 | non déployés — draft en attente de validation |
| `TEST_NEGATIVE` | 5 | packets de test négatif (validation contraintes) |
| `TEST_POSITIVE` | 1 | packet de test positif |
| `WRITE_GATED` | 1 | packet actif avec gate écriture |
| `DRY_RUN_PENDING_APPROVAL` | 1 | dry-run en attente d'approbation opérateur |

| Famille task_type | Count | Exemples |
|---|---|---|
| `WRITE_GATED` | 8 | GO_STRICT_WORKERS_WRITE_GATED_* |
| non typé | 7 | GO_STRICT_WORKERS_A4_NEGATIVE_* |
| `READ_INVENTORY` | 6 | GO_STRICT_WORKERS_READ_INVENTORY_* |
| `PATCH_DRAFT` | 3 | GO_STRICT_WORKERS_PATCH_DRAFT_* |
| `FAST_TRIAGE` | 2 | GO_STRICT_WORKERS_E2E_FAST_TRIAGE_* |
| autres | 4 | ENDPOINT_AUDIT, TESTPLAN, CHERRY_PICK, DOC_DRAFT |

Entrées notables :

| job_id | path | status | task_type | next_action |
|---|---|---|---|---|
| `jp_drive_canary` | `job_packets/GO_DRIVE_CANARY_PACKET_01.json` | WRITE_GATED | WRITE_GATED | keep |
| `jp_strict_readonly_smoke` | `job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json` | candidate | READ_INVENTORY | keep |
| `jp_strict_pool_smoke_deepseek` | `job_packets/GO_STRICT_WORKERS_POOL_SMOKE_DEEPSEEK_V4_FLASH_FREE.json` | candidate | READ_INVENTORY | keep |
| `jp_strict_pool_smoke_ring` | `job_packets/GO_STRICT_WORKERS_POOL_SMOKE_RING_2_6_1T_FREE.json` | deprecated | READ_INVENTORY | — (worker=deepseek, nom trompeur) |
| `jp_strict_pool_smoke_trinity` | `job_packets/GO_STRICT_WORKERS_POOL_SMOKE_TRINITY_LARGE_PREVIEW_FREE.json` | deprecated | READ_INVENTORY | — (worker=nemotron, nom trompeur) |
| `jp_doc_ops_*` | `job_packets/GO_OPT_TRADING_DOC_OPS_*` (8) | DRAFT_ONLY | varies | blocked_review |
| `jp_strict_a4_negative_*` | `job_packets/GO_STRICT_WORKERS_A4_NEGATIVE_*` (5) | TEST_NEGATIVE | — | keep (tests) |

---

## Section 4 — AI workers — scripts Python (26)

| job_id | path | type | owner_surface | rôle | status | risk | next_action |
|---|---|---|---|---|---|---|---|
| `aw_ledger_writer` | `scripts/ai/workers/ledger_writer.py` | python | ai_workers | écriture ledger events | active | high | keep |
| `aw_ledger_replay` | `scripts/ai/workers/ledger_replay.py` | python | ai_workers | replay événements ledger | active | medium | keep |
| `aw_ledger_rotation` | `scripts/ai/workers/ledger_rotation_check.py` | python | ai_workers | rotation et archivage | active | medium | keep |
| `aw_ledger_schema` | `scripts/ai/workers/ledger_schema_validation.py` | python | ai_workers | validation schéma ledger | active | medium | keep |
| `aw_ledger_trace` | `scripts/ai/workers/ledger_trace_id_audit.py` | python | ai_workers | audit trace IDs | active | low | keep |
| `aw_ledger_blocked` | `scripts/ai/workers/ledger_blocked_events_digest.py` | python | ai_workers | digest événements bloqués | active | low | keep |
| `aw_doc_ops_constraint` | `scripts/ai/workers/doc_ops_constraint_check.py` | python | ai_workers | vérifie contraintes doc ops | active | low | keep |
| `aw_doc_ops_create` | `scripts/ai/workers/doc_ops_create_chantier.py` | python | ai_workers | crée chantier doc | active | medium | keep |
| `aw_doc_ops_index` | `scripts/ai/workers/doc_ops_go_index_insert.py` | python | ai_workers | insère dans GO index | active | medium | keep |
| `aw_strict_denied_scan` | `scripts/ai/workers/strict_worker_denied_command_scan.py` | python | ai_workers | scan commandes interdites | active | medium | keep |
| `aw_strict_log_archive` | `scripts/ai/workers/strict_worker_log_archive.py` | python | ai_workers | archivage logs strict | active | low | keep |
| `aw_strict_output_schema` | `scripts/ai/workers/strict_worker_output_schema_check.py` | python | ai_workers | valide schema output | active | medium | keep |
| `aw_signal_processor` | `scripts/ai/workers/signal_processor.py` | python | ai_workers | traitement signaux | candidate | high | keep |
| `aw_signal_stats` | `scripts/ai/workers/signal_stats.py` | python | ai_workers | stats signaux | candidate | medium | keep |
| `aw_health_status` | `scripts/ai/workers/health_status.py` | python | ai_workers | état santé système | active | low | keep |
| `aw_stuck_job` | `scripts/ai/workers/stuck_job_detector.py` | python | ai_workers | détecte jobs bloqués | active | medium | keep |
| `aw_permission_drift` | `scripts/ai/workers/permission_drift_check.py` | python | ai_workers | audit dérives permissions | active | medium | keep |
| `aw_oauth_audit` | `scripts/ai/workers/oauth_scope_audit.py` | python | ai_workers | audit scopes OAuth | candidate | high | add_test |
| `aw_repo_frontmatter` | `scripts/ai/workers/repo_doc_frontmatter_lint.py` | python | ai_workers | lint frontmatter docs | active | low | keep |
| `aw_repo_link_check` | `scripts/ai/workers/repo_doc_link_check.py` | python | ai_workers | vérifie liens docs | active | low | keep |
| `aw_kill_switch` | `scripts/ai/workers/kill_switch_fullstop_test.py` | python | ai_workers | test kill switch | active | high | keep |
| `aw_localcms_sync` | `scripts/ai/workers/localcms_automation_status_sync.py` | python | ai_workers | sync status localcms | candidate | medium | keep |
| `aw_openclaw_mobile` | `scripts/ai/workers/openclaw_mobile_control.py` | python | ai_workers | contrôle mobile openclaw | candidate | medium | keep |
| `aw_runner_readonly` | `scripts/ai/workers/runner_readonly.py` | python | ai_workers | runner lecture seule | active | low | keep |

---

## Section 5 — OpenClaw scripts opérateurs

| job_id | path | type | trigger | owner_surface | outputs | status | risk | next_action |
|---|---|---|---|---|---|---|---|---|
| `oc_gateway_start` | `modules/gateway_openclaw/scripts/start.sh` | shell | manual | openclaw | session tmux openclaw-gateway | active | medium | keep |
| `oc_gateway_stop` | `modules/gateway_openclaw/scripts/stop.sh` | shell | manual | openclaw | session tmux fermée | active | medium | keep |
| `oc_gateway_attach` | `modules/gateway_openclaw/scripts/attach.sh` | shell | manual | openclaw | — | active | low | keep |
| `oc_gateway_logs` | `modules/gateway_openclaw/scripts/logs.sh` | shell | manual | openclaw | logs tmux | active | low | keep |
| `oc_config_apply` | `modules/openclaw_config_modulaire/scripts/apply_safe.sh` | shell | manual | openclaw | ~/.openclaw/config.d/ modifié | active | high | keep |
| `oc_config_rollback` | `modules/openclaw_config_modulaire/scripts/rollback.sh` | shell | manual | openclaw | config restaurée | active | high | keep |
| `oc_tmux_operator` | `modules/openclaw_tmux_operator/scripts/cmd.sh` | shell | manual / openclaw_call | openclaw | commandes tmux | active | medium | keep |

---

## Section 6 — Scripts legacy patch desk_pro (DELETED)

| job_id | path | type | status | preuve | next_action |
|---|---|---|---|---|---|
| `dp_toolbox_patch` | `scripts/apply_desk_pro_toolbox_patch.sh` | shell | deleted | routes.py:299-354 patché — GO_CLEANUP_LEGACY_SCRIPTS_01 | — |
| `dp_ui_inject_patch` | `scripts/apply_desk_pro_ui_inject_patch.sh` | shell | deleted | routes.py:299-354 patché — GO_CLEANUP_LEGACY_SCRIPTS_01 | — |
| `dp_ui_plus_patch` | `scripts/apply_desk_pro_ui_plus_patch.sh` | shell | deleted | routes.py:299-354 patché — GO_CLEANUP_LEGACY_SCRIPTS_01 | — |
| `dp_ui_toolbox_fix` | `scripts/apply_desk_pro_ui_toolbox_fix.sh` | shell | deleted | routes.py:299-354 patché — GO_CLEANUP_LEGACY_SCRIPTS_01 | — |
| `dp_ui_toolbox_fix_v2` | `scripts/apply_desk_pro_ui_toolbox_fix_v2.sh` | shell | deleted | routes.py:299-354 patché — GO_CLEANUP_LEGACY_SCRIPTS_01 | — |
| `dp_ui_toolbox_fix_v3` | `scripts/apply_desk_pro_ui_toolbox_fix_v3.sh` | shell | deleted | routes.py:299-354 patché — GO_CLEANUP_LEGACY_SCRIPTS_01 | — |
| `dp_ui_toolbox_fix_v4` | `scripts/apply_desk_pro_ui_toolbox_fix_v4.sh` | shell | deleted | routes.py:299-354 patché — GO_CLEANUP_LEGACY_SCRIPTS_01 | — |
| `dp_ui_toolbox_final` | `scripts/apply_desk_pro_ui_toolbox_final.sh` | shell | deleted | routes.py:299-354 patché — GO_CLEANUP_LEGACY_SCRIPTS_01 | — |

---

## Section 7 — Scripts opérateurs racine (clés)

| job_id | path | type | trigger | owner_surface | status | risk | next_action |
|---|---|---|---|---|---|---|---|
| `op_verify_all` | `scripts/verify_all.sh` | shell | manual | ops | active | low | keep |
| `op_smoke` | `scripts/smoke.sh` | shell | manual / ci | ops | active | low | keep |
| `op_diagnose` | `scripts/diagnose.sh` | shell | manual | ops | active | low | keep |
| `op_post_change` | `scripts/post_change.sh` | shell | manual | ops | active | low | keep |
| `op_deploy_wrappers` | `scripts/deploy_wrappers_ot_wrap_01.sh` | shell | manual | ops | candidate | medium | keep |
| `op_desk_pro_cmd` | `scripts/desk_pro_cmd.sh` | shell | manual | desk_pro | active | medium | keep |

---

## Anomalies à traiter (lots dédiés)

| anomalie_id | description | lot requis |
|---|---|---|
| B01 | tasks.index.json en DRAFT_ONLY — pas de registre formel | formaliser dans jobs dedup audit |
| B02 | 22 job_packets DRAFT_ONLY sans owner ni test | GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01 |
| B03 | orchestration/ contrat non connecté aux workers | qualifier en dedup audit |
| B04 | signal_processor + oauth_scope_audit sans test | ADD_TEST batch dédié |
| B05 | gha_strict_workers_schedule sans test unitaire | ADD_TEST batch dédié |
| B06 | 8 scripts apply_desk_pro_*.sh — LEGACY_REPLACED | DELETE — batch GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01 |

---

## Statistiques v1

| Catégorie | Count |
|---|---|
| GHA workflows | 7 |
| AI worker entry points | 4 (run_task + validate + 2 configs) |
| job_packets | 30 |
| AI workers Python | 24 |
| OpenClaw scripts | 7 |
| Scripts opérateurs racine clés | 6 |
| Scripts legacy patch deprecated (B06) | 8 |
| **Total référencé v1** | **~86** |

| Statut | Count |
|---|---|
| active | ~45 |
| candidate | ~10 (+2 : jp_strict_readonly_smoke, jp_strict_pool_smoke_deepseek) |
| deprecated | ~12 (+2 : jp_strict_pool_smoke_ring, jp_strict_pool_smoke_trinity) |
| experimental | 2 |
| DRAFT_ONLY (pending_parent) | ~16 (MATRIX×8, PATCH_IMPL×1, DOC_OPS×7) |

> Dernière mise à jour 2026-05-28 — v1.3 : ADD_TEST_SIGNAL_SCHEDULE_BATCH_01 — aw_signal_processor + aw_signal_stats : add_test → keep (34 tests) ; gha_strict_workers_schedule : add_test → keep. GO_OPT_TRADING_CHILD_ADD_TEST_SIGNAL_SCHEDULE_BATCH_01.
