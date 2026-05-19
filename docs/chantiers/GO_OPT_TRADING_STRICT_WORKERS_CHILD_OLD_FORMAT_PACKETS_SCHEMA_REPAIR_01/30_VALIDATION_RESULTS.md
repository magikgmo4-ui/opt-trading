# Validation Results

## Commande

```bash
for f in scripts/ai/workers/job_packets/*.json; do
  TASKS_INDEX_PATH=... MODELS_REGISTRY_PATH=... JOB_PACKET_PATH=$f \
    OUTPUT_DIR_PATH=reports/ai/workers REPO_ROOT=$(pwd) \
    python3 scripts/ai/workers/_validate_job.py
done
```

## Résultat

```
PASS=22 FAIL=0
```

## Vérifications additionnelles

- `git diff --check` : 0 whitespace errors
- Aucun modèle RETIRED / ABSENT / OBSOLETE dans `worker_candidates` ou `default_worker`
- Scope limité aux chemins autorisés
- `tasks.index.json` : non modifié
- `models.registry.json` : non modifié
- `_validate_job.py` : non modifié
