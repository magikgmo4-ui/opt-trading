# STRICT WORKER REPORT — TESTPLAN

## TESTS_UNITAIRES

| ID | Test | Cible | Commande |
|---|---|---|---|
| U1 | Validation schema packet | Chaque job packet JSON | `TASKS_INDEX_PATH=... MODELS_REGISTRY_PATH=... JOB_PACKET_PATH=... OUTPUT_DIR_PATH=... python3 scripts/ai/workers/_validate_job.py` |
| U2 | Runner lock git clean | run_task.sh | `bash scripts/ai/workers/run_task.sh <packet>` sur working tree propre (exit 0) |
| U3 | Runner lock git dirty | run_task.sh | `bash scripts/ai/workers/run_task.sh <packet>` sur working tree sale (exit 2, BLOCKED) |
| U4 | Modele registry integrity | models.registry.json | `python3 -c "import json; d=json.load(open('scripts/ai/workers/models.registry.json')); assert all(v.get('config_id') for k,v in d['models'].items() if v['status']=='VERIFIED')"` |
| U5 | Task index completude | tasks.index.json | `python3 -c "import json; d=json.load(open('scripts/ai/workers/tasks.index.json')); assert len(d['tasks']) == 8"` |

## TESTS_SMOKE

| ID | Test | Cible | Commande |
|---|---|---|---|
| S1 | Validation batch 22 packets | Tous les job packets | `for f in scripts/ai/workers/job_packets/*.json; do TASKS_INDEX_PATH=... MODELS_REGISTRY_PATH=... JOB_PACKET_PATH=$f OUTPUT_DIR_PATH=reports/ai/workers python3 scripts/ai/workers/_validate_job.py || exit 1; done` |
| S2 | Run READ_INVENTORY complet | GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01 | `bash scripts/ai/workers/run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01.json` |
| S3 | Run FAST_TRIAGE complet | GO_STRICT_WORKERS_FAST_TRIAGE_MATRIX_01 | Meme pattern que S2 |
| S4 | Endpoint reachable | opencode.ai API | `curl -s -o /dev/null -w '%{http_code}' https://opencode.ai/zen/v1/models` (attend 200) |

## COMMANDES

```bash
# Validation unique
TASKS_INDEX_PATH=scripts/ai/workers/tasks.index.json \
MODELS_REGISTRY_PATH=scripts/ai/workers/models.registry.json \
JOB_PACKET_PATH=scripts/ai/workers/job_packets/GO_STRICT_WORKERS_TESTPLAN_MATRIX_01.json \
OUTPUT_DIR_PATH=reports/ai/workers \
python3 scripts/ai/workers/_validate_job.py

# Run complet
bash scripts/ai/workers/run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_TESTPLAN_MATRIX_01.json

# Batch validation CI/CD (comme dans strict-workers-validate.yml)
for packet in scripts/ai/workers/job_packets/*.json; do
  export JOB_PACKET_PATH="$packet"
  python3 scripts/ai/workers/_validate_job.py || exit 1
done
```

## CRITERES_PASS_FAIL

| Criteres | Pass | Fail |
|---|---|---|
| Validation schema | Tous les champs requis presents | MISSING_FIELD, UNKNOWN_TASK_TYPE |
| Workers verifies | default_worker dans VERIFIED candidats | DEFAULT_WORKER_NOT_VERIFIED, NO_VERIFIED_WORKER |
| Inputs files | Glob patterns matchent des fichiers existants | INPUT_NOT_FOUND |
| Output path | output_file correspond a un allowed_output | OUTPUT_NOT_ALLOWED |
| Denied inputs | Aucun allowed_input ne match un denied pattern | DENIED_INPUT |
| Git clean | git status --porcelain est vide | BLOCKED (exit 2) |

## RISQUES_RESTANTS

1. VERIFIED_FREE models (nemotron-3-super-free, deepseek-v4-flash-free, etc.) passes la validation mais ne sont pas dans valid_workers — ils ne peuvent pas etre default_worker
2. Les globs larges (docs/**, scripts/**, modules/**) passent INPUT_NOT_FOUND check mais peuvent matcher des fichiers sensibles par accident (ex: un fichier *secret* dans modules/)
3. Aucun test CI/CD n execute le worker model (inference) — seuls le schema et le runner lock sont valides automatiquement
4. ring-2.6-1t-free et trinity-large-preview-free sont retirees de l endpoint mais toujours referencees dans 3 job packets — la smoke CI/CD (qui utilise l endpoint) echouera

## VERDICT_DRAFT_ONLY
