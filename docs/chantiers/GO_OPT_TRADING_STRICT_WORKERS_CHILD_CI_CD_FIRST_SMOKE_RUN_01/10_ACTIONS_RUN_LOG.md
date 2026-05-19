# 10_ACTIONS_RUN_LOG — Premier déclenchement des workflows

## Run IDs

| Workflow | Run ID | URL |
|----------|--------|-----|
| Validate | 26094375920 | https://github.com/magikgmo4-ui/opt-trading/actions/runs/26094375920 |
| Smoke | 26094378693 | https://github.com/magikgmo4-ui/opt-trading/actions/runs/26094378693 |

## Résultat initial

```
Validate: conclusion=failure, status=completed
Smoke:    conclusion=failure, status=completed
```

### Validate — Cause du failure

```text
KeyError: 'TASKS_INDEX_PATH'
  File "scripts/ai/workers/_validate_job.py", line 5
    tasks_idx = os.environ['TASKS_INDEX_PATH']
```

Le validateur attend 4 variables d'environnement (`TASKS_INDEX_PATH`, `MODELS_REGISTRY_PATH`, `JOB_PACKET_PATH`, `OUTPUT_DIR_PATH`) qui n'étaient pas définies dans le workflow CI.

### Smoke — Cause du failure

```text
ERROR: Job packet not found: --job-packet
```

Le runner `run_task.sh` utilise un argument positionnel (`Usage: ./run_task.sh <job_packet.json>`) mais le workflow passait `--job-packet` comme flag.

## Correction appliquée

### validate.yml
- Ajout des env vars `TASKS_INDEX_PATH`, `MODELS_REGISTRY_PATH`, `OUTPUT_DIR_PATH` au step
- Utilisation de `export JOB_PACKET_PATH="$packet"` dans la boucle
- Appel sans argument (le script lit JOB_PACKET_PATH depuis l'env)

### smoke.yml
- Remplacement de `--job-packet <path>` par `<path>` en argument positionnel
- Suppression de `--dry-run` (le runner n'a pas ce flag)
