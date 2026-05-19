---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_JOB_PACKETS_PROMOTION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_JOB_PACKETS_PROMOTION_01
status: draft_canonical
lifecycle_stage: draft
topic_keys:
  - opt-trading
  - strict_workers
  - job_packets
  - promotion
  - json
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/40_JOB_PACKET_DRAFTS.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/20_JOB_PACKETS_SPEC.md
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
  - scripts/ai/workers/_validate_job.py
  - scripts/ai/workers/run_task.sh
---

# 00_INITIAL_PROJECT_DOC

## Objectif

Promouvoir les 8 drafts JSON de job packets stockes dans le fichier Markdown
40_JOB_PACKET_DRAFTS.md vers de vrais fichiers JSON dans
scripts/ai/workers/job_packets/, validables par les workflows CI/CD merges.

Les drafts sont au nombre de 8, correspondant aux 8 task types definis dans
tasks.index.json (schema_version 0.3-draft).

## Source des drafts

Les drafts JSON se trouvent dans:
docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/40_JOB_PACKET_DRAFTS.md

Chaque draft est un bloc JSON avec des champs au format worker-pool-extension
(task, model, fallback_models, inputs, output, validation, etc.).
La promotion convertit ces drafts au format validable par _validate_job.py
(task_type, worker_candidates, default_worker, scope, etc.).

## Job packets a promouvoir

| # | job_packet_id | task_type | default_worker |
|---|---|---|---|
| 1 | GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01 | READ_INVENTORY | qwen3.5-plus |
| 2 | GO_STRICT_WORKERS_PATCH_DRAFT_MATRIX_01 | PATCH_DRAFT | glm-5.1 |
| 3 | GO_STRICT_WORKERS_DOC_DRAFT_MATRIX_01 | DOC_DRAFT | qwen3.5-plus |
| 4 | GO_STRICT_WORKERS_TESTPLAN_MATRIX_01 | TESTPLAN | glm-5.1 |
| 5 | GO_STRICT_WORKERS_CHERRY_PICK_INVENTORY_MATRIX_01 | CHERRY_PICK_INVENTORY | kimi-k2.5 |
| 6 | GO_STRICT_WORKERS_FAST_TRIAGE_MATRIX_01 | FAST_TRIAGE | qwen3.5-plus |
| 7 | GO_STRICT_WORKERS_ENDPOINT_AUDIT_MATRIX_01 | ENDPOINT_AUDIT | qwen3.5-plus |
| 8 | GO_STRICT_WORKERS_WRITE_GATED_DRYRUN_MATRIX_01 | WRITE_GATED | glm-5.1 |

## Schema cible

Chaque fichier JSON suit le schema exact observe dans les packets existants
(eg. GO_STRICT_WORKERS_READONLY_SMOKE_01.json):

- job_packet_id, go_id, status, task_type
- worker_candidates (liste de noms de modeles sans prefixe opencode/)
- default_worker
- model_registry, task_index (chemins vers les fichiers)
- scope: allowed_inputs, denied_inputs_inherited, allowed_outputs
- instructions (liste de consignes en Markdown)
- required_output_sections
- acceptance (criteres specifiques par type de tache)

## Contraintes

- Tout job packet reste DRAFT_ONLY, pas de run externe
- denied_inputs_inherited: true pour heriter des patterns de tasks.index.json
- worker_candidates limites aux modeles VERIFIED / VERIFIED_FREE du registry
- Scope: pas de wildcard pour allowed_inputs/allowed_outputs
