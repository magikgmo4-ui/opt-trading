# Diagnostic des 12 packets invalides

## Règle du validateur

Le validateur (`_validate_job.py:17`) exige ces champs dans tout job packet :

```
job_packet_id, task_type, worker_candidates, default_worker, scope
```

Et `default_worker` doit être dans `worker_candidates` ET avoir `status == "VERIFIED"` dans le registry.

## Packets POOL_SMOKE (3)

| Packet | worker_assigned | Problème | Correction |
|---|---|---|---|
| `POOL_SMOKE_DEEPSEEK_V4_FLASH_FREE` | `deepseek-v4-flash-free` (VERIFIED_FREE) | Manque `worker_candidates` + `default_worker` | Ajout `["qwen3.5-plus", "deepseek-v4-flash-free"]` / `qwen3.5-plus` |
| `POOL_SMOKE_RING_2_6_1T_FREE` | `ring-2.6-1t-free` (RETIRED) | Modèle retiré de l'endpoint | Reassigné à `deepseek-v4-flash-free` |
| `POOL_SMOKE_TRINITY_LARGE_PREVIEW_FREE` | `trinity-large-preview-free` (RETIRED) | Modèle retiré de l'endpoint | Reassigné à `nemotron-3-super-free` |

## Packets E2E (2)

| Packet | worker_assigned | Problème | Correction |
|---|---|---|---|
| `E2E_READ_INVENTORY_A` | `minimax-m2.5` (VERIFIED) | Manque `worker_candidates` + `default_worker` | Ajout `["minimax-m2.5"]` / `minimax-m2.5` |
| `E2E_FAST_TRIAGE_B` | `qwen3.5-plus` (VERIFIED) | Manque `worker_candidates` + `default_worker` | Ajout `["qwen3.5-plus"]` / `qwen3.5-plus` |

## Packets A4 (7)

| Packet | task_type | worker_assigned | Problème | Correction |
|---|---|---|---|---|
| `A4_NEGATIVE_N1_NO_APPROVAL` | WRITE_GATED | `glm-5.1` | Manque champs + allowed_outputs mismatch | Ajout champs + fix output path |
| `A4_NEGATIVE_N2_OUTSIDE_ALLOWLIST` | WRITE_GATED | `qwen3.6-plus` | Manque champs + allowed_outputs = modules/ | Ajout champs + fix output path |
| `A4_NEGATIVE_N3_S3CR3T_INPUT` | WRITE_GATED | `big-pickle` | Manque champs + allowed_inputs = denied pattern | Ajout champs + allowed_inputs sûr |
| `A4_NEGATIVE_N4_GLOBAL_INDEX` | WRITE_GATED | `glm-5.1` | Manque champs + pas de allowed_outputs | Ajout champs + fix output path |
| `A4_NEGATIVE_N5_PATCH_DRAFT_WRITE` | PATCH_DRAFT | `glm-5.1` | Manque champs + allowed_outputs hors reports | Ajout champs + fix output path |
| `A4_POSITIVE_P6_GATED_WRITE` | WRITE_GATED | `glm-5.1` | Manque champs + allowed_outputs mismatch | Ajout champs + fix output path |
| `A4_WRITE_REEL_TEST` | WRITE_GATED | `glm-5.1` | Manque `worker_candidates` + `default_worker` | Ajout champs |
