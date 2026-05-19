# STRICT WORKER REPORT — PATCH_DRAFT

## OBJECTIF_PATCH

Mettre a jour models.registry.json suite a l ENDPOINT_AUDIT:
1. ring-2.6-1t-free: VERIFIED_FREE → RETIRED_CURRENT_ENDPOINT (retire de l endpoint)
2. trinity-large-preview-free: VERIFIED_FREE → RETIRED_CURRENT_ENDPOINT (retire de l endpoint)
3. Mettre a jour validated_at: "2026-05-19"
4. Ajouter note de migration pour les 2 modeles retires

## FICHIERS_TOUCHES

- scripts/ai/workers/models.registry.json (modification)
- Aucun autre fichier modifie

## DIFF_ATTENDU

```diff
--- a/scripts/ai/workers/models.registry.json
+++ b/scripts/ai/workers/models.registry.json
@@ -4,7 +4,7 @@
   "parent_go_id": "GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01",
   "validation_source": "https://opencode.ai/zen/v1/models",
-  "validated_at": "2026-05-14",
+  "validated_at": "2026-05-19",
   "previous_validated_at": "2026-04-26",
@@ -22,8 +22,8 @@
-    "ring-2.6-1t-free": {"config_id": "opencode/ring-2.6-1t-free", "status": "VERIFIED_FREE", "autonomy_max": "A1", "roles": ["READ_INVENTORY", "FAST_TRIAGE"], "note": "Nouveau dans l'endpoint. Possible successeur de ling-2.6-flash-free (retire)."},
-    "trinity-large-preview-free": {"config_id": "opencode/trinity-large-preview-free", "status": "VERIFIED_FREE", "autonomy_max": "A1", "roles": ["READ_INVENTORY"], "note": "Nouveau dans l'endpoint. Usage conservatif A1 uniquement."},
+    "ring-2.6-1t-free": {"config_id": "opencode/ring-2.6-1t-free", "status": "RETIRED_CURRENT_ENDPOINT", "autonomy_max": "A0", "roles": [], "note": "Retire de l'endpoint au 2026-05-19. Etait VERIFIED_FREE depuis 2026-05-14."},
+    "trinity-large-preview-free": {"config_id": "opencode/trinity-large-preview-free", "status": "RETIRED_CURRENT_ENDPOINT", "autonomy_max": "A0", "roles": [], "note": "Retire de l'endpoint au 2026-05-19. Etait VERIFIED_FREE depuis 2026-05-14. Usage conservatif A1."},
```

Total diff: ~12 lignes (dans limite 100 lignes)

## RISQUES

1. Les 2 modeles retirees sont references dans des job packets existants:
   - GO_STRICT_WORKERS_POOL_SMOKE_RING_2_6_1T_FREE.json
   - GO_STRICT_WORKERS_POOL_SMOKE_TRINITY_LARGE_PREVIEW_FREE.json
   - GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01.json (ring est dans worker_candidates)
   - GO_STRICT_WORKERS_FAST_TRIAGE_MATRIX_01.json (ring est dans worker_candidates)
   Ces packets continueront de valider (registry a une entree RETIRED) mais le runner echouera si tente d utiliser ces modeles
2. Modifier le registry affecte tous les job packets qui le referencent — valider avec _validate_job.py apres le patch

## TESTS_A_EXECUTER

1. `python3 -c "import json; json.load(open('scripts/ai/workers/models.registry.json'))"` — JSON valide
2. `TASKS_INDEX_PATH=... MODELS_REGISTRY_PATH=... JOB_PACKET_PATH=.../GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01.json OUTPUT_DIR_PATH=... python3 scripts/ai/workers/_validate_job.py` — validation READ_INVENTORY passe toujours
3. `TASKS_INDEX_PATH=... MODELS_REGISTRY_PATH=... JOB_PACKET_PATH=.../GO_STRICT_WORKERS_POOL_SMOKE_RING_2_6_1T_FREE.json OUTPUT_DIR_PATH=... python3 scripts/ai/workers/_validate_job.py` — validation POOL_SMOKE_RING passe toujours (le modele existe encore dans le registry, juste RETIRED)
4. `bash scripts/ai/workers/run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01.json` — run complete toujours

## VERDICT_DRAFT_ONLY
