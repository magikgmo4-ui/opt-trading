---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01_INVENTORY
doc_type: packet_inventory
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01
created_at: 2026-05-28
source: scripts/ai/workers/job_packets/ (30 fichiers)
---

# 10_PACKET_INVENTORY

## 1_TOTAL_FICHIERS

| Statut | Count |
|--------|------:|
| DRAFT_ONLY analysables | 20 |
| TEST_NEGATIVE | 5 |
| TEST_POSITIVE | 1 |
| WRITE_GATED opérationnel | 1 |
| DRY_RUN_PENDING_APPROVAL | 1 |
| E2E fixtures (opérationnels) | 2 |
| **Total fichiers** | **30** |

## 2_FAMILLES_DRAFT_ONLY

### Famille A — READONLY_SMOKE (1 packet)

| Fichier | go_id | task_type | worker_default |
|---------|-------|-----------|----------------|
| `GO_STRICT_WORKERS_READONLY_SMOKE_01.json` | `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | READ_INVENTORY | qwen3.5-plus |

- Inputs référencés : `docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md`, `MODELS_MATRIX_01.md`, `MODEL_ID_VALIDATION_01.md`, `tasks.index.json`, `models.registry.json`
- Workers : `qwen3.5-plus` (VERIFIED), `minimax-m2.5` (VERIFIED), `kimi-k2.5` (VERIFIED), `big-pickle` (VERIFIED), `gpt-5-nano` (VERIFIED)

### Famille B — POOL_SMOKE (3 packets)

| Fichier | worker_assigned | worker_status (models.registry) |
|---------|----------------|--------------------------------|
| `GO_STRICT_WORKERS_POOL_SMOKE_DEEPSEEK_V4_FLASH_FREE.json` | `deepseek-v4-flash-free` | **VERIFIED_FREE** |
| `GO_STRICT_WORKERS_POOL_SMOKE_RING_2_6_1T_FREE.json` | `ring-2.6-1t-free` | **RETIRED_CURRENT_ENDPOINT** |
| `GO_STRICT_WORKERS_POOL_SMOKE_TRINITY_LARGE_PREVIEW_FREE.json` | `trinity-large-preview-free` | **RETIRED_CURRENT_ENDPOINT** |

go_id commun : `GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01`

### Famille C — STRICT_WORKERS_MATRIX (8 packets)

go_id commun : `GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01` (status: **cadrage**)

| Fichier | task_type |
|---------|-----------|
| `GO_STRICT_WORKERS_CHERRY_PICK_INVENTORY_MATRIX_01.json` | CHERRY_PICK_INVENTORY |
| `GO_STRICT_WORKERS_DOC_DRAFT_MATRIX_01.json` | DOC_DRAFT |
| `GO_STRICT_WORKERS_ENDPOINT_AUDIT_MATRIX_01.json` | ENDPOINT_AUDIT |
| `GO_STRICT_WORKERS_FAST_TRIAGE_MATRIX_01.json` | FAST_TRIAGE |
| `GO_STRICT_WORKERS_PATCH_DRAFT_MATRIX_01.json` | PATCH_DRAFT |
| `GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01.json` | READ_INVENTORY |
| `GO_STRICT_WORKERS_TESTPLAN_MATRIX_01.json` | TESTPLAN |
| `GO_STRICT_WORKERS_WRITE_GATED_DRYRUN_MATRIX_01.json` | WRITE_GATED |

### Famille D — PATCH_DRAFT_IMPL (1 packet)

| Fichier | go_id | task_type |
|---------|-------|-----------|
| `GO_STRICT_WORKERS_PATCH_DRAFT_IMPL_01.json` | `GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01` (status: **cadrage**) | PATCH_DRAFT |

### Famille E — DOC_OPS (7 packets)

go_id commun : `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01` (status: **draft_canonical**)

| Fichier | task_type |
|---------|-----------|
| `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_DOC_DRAFT_01.json` | DOC_DRAFT |
| `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_ENDPOINT_AUDIT_01.json` | ENDPOINT_AUDIT |
| `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_FAST_TRIAGE_01.json` | FAST_TRIAGE |
| `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_PATCH_DRAFT_01.json` | PATCH_DRAFT |
| `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_READ_INVENTORY_01.json` | READ_INVENTORY |
| `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_TESTPLAN_01.json` | TESTPLAN |
| `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_WRITE_GATED_01.json` | WRITE_GATED |

## 3_RÉSUMÉ_PAR_FAMILLE

| Famille | Count | Parent GO status | Verdict préliminaire |
|---------|------:|-----------------|----------------------|
| A — READONLY_SMOKE | 1 | STRICT_WORKERS_PARENT (actif) | promote_candidate |
| B — POOL_SMOKE deepseek | 1 | POOL_SMOKE (actif) | promote_candidate |
| B — POOL_SMOKE ring/trinity | 2 | POOL_SMOKE (actif) | deprecate — worker RETIRED |
| C — MATRIX | 8 | POOL_EXTENSION (cadrage) | pending_parent |
| D — PATCH_DRAFT_IMPL | 1 | RUNTIME_LOCK (cadrage) | pending_parent |
| E — DOC_OPS | 7 | DOC_OPS_PATCH_ZIP (draft_canonical) | pending_parent |
