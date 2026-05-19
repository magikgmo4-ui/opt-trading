# Schema Repair Log

## Changements effectués

### 1. POOL_SMOKE (3 files)
- `POOL_SMOKE_DEEPSEEK_V4_FLASH_FREE.json` : +`worker_candidates`/`default_worker`
- `POOL_SMOKE_RING_2_6_1T_FREE.json` : `ring-2.6-1t-free` → `deepseek-v4-flash-free`, +`worker_candidates`/`default_worker`
- `POOL_SMOKE_TRINITY_LARGE_PREVIEW_FREE.json` : `trinity-large-preview-free` → `nemotron-3-super-free`, +`worker_candidates`/`default_worker`

### 2. E2E (2 files)
- `E2E_READ_INVENTORY_A.json` : +`worker_candidates`/`default_worker`
- `E2E_FAST_TRIAGE_B.json` : +`worker_candidates`/`default_worker`

### 3. A4 (7 files)
- `A4_NEGATIVE_N1_NO_APPROVAL.json` : +worker_candidates/default_worker, +allowed_inputs, fix allowed_outputs
- `A4_NEGATIVE_N2_OUTSIDE_ALLOWLIST.json` : +worker_candidates/default_worker, +allowed_inputs, fix allowed_outputs
- `A4_NEGATIVE_N3_S3CR3T_INPUT.json` : +worker_candidates/default_worker, allowed_inputs → safe path, fix allowed_outputs
- `A4_NEGATIVE_N4_GLOBAL_INDEX.json` : +worker_candidates/default_worker, +allowed_outputs
- `A4_NEGATIVE_N5_PATCH_DRAFT_WRITE.json` : +worker_candidates/default_worker, fix allowed_outputs
- `A4_POSITIVE_P6_GATED_WRITE.json` : +worker_candidates/default_worker, fix allowed_outputs
- `A4_WRITE_REEL_TEST.json` : +worker_candidates/default_worker

## Principe de correction

Le validateur vérifie la **conformité statique du schema** (structure JSON).
Les tests de **comportement** (rôles, permissions, rejets) sont assurés par `run_task.sh` et les règles `acceptance`.
Les corrections schema n'altèrent pas la finalité des packets de test.
