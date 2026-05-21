---
doc_id: GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01_SMOKE_RESULT
doc_type: smoke_result
go_id: GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01
status: PASS
lifecycle_stage: validation
---

# 20_SMOKE_RESULT — read-only runner validation

## Runner

`scripts/ai/workers/runner_readonly.py`

## Job packet

`scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json`

## Dry-run mode

```text
COMMAND: python3 runner_readonly.py <packet> --dry-run
STATUS: DRY_RUN_PASS
MUTATIONS: 0
```

## Real execution

```text
COMMAND: python3 runner_readonly.py <packet>
STATUS: PASS
READS: 5 files (3004 + 8600 + 4545 + 4773 + 4425 bytes)
WRITES: 0 (blocked: none attempted)
```

| File read | Size |
|---|---|
| docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md | 3004 B |
| docs/agents/strict_workers/MODELS_MATRIX_01.md | 8600 B |
| docs/agents/strict_workers/MODEL_ID_VALIDATION_01.md | 4545 B |
| scripts/ai/workers/tasks.index.json | 4773 B |
| scripts/ai/workers/models.registry.json | 4425 B |

## Outputs

- `reports/ai/workers/GO_STRICT_WORKERS_READONLY_SMOKE_01_RUNNER.json` (normalized JSON output)
- `data/runtime_health/job_logs/GO_STRICT_WORKERS_READONLY_SMOKE_01.json` (per-job log)

## No-write guard

- Aucune tentative d'écriture détectée
- Aucune mutation repo
- Aucune modification des fichiers suivis

## Verdict

```text
G02_STRICT_WORKERS_RUNTIME: PASS_WITH_EVIDENCE
preuve: smoke réussi (5 reads, 0 writes)
runner: scripts/ai/workers/runner_readonly.py
```
