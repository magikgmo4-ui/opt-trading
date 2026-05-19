---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_JOB_PACKET_FIRST_REAL_RUN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_JOB_PACKET_FIRST_REAL_RUN_01
status: draft_canonical
lifecycle_stage: draft
topic_keys:
  - opt-trading
  - strict_workers
  - real_run
  - read_inventory
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01.json
  - scripts/ai/workers/run_task.sh
  - scripts/ai/workers/_validate_job.py
  - reports/ai/workers/GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01.md
---

# 00_INITIAL_PROJECT_DOC

## Objectif

Executer le premier run reel controle du job packet promu READ_INVENTORY.

## Packet cible

- Fichier: scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01.json
- Task type: READ_INVENTORY
- Default worker: qwen3.5-plus
- Autonomy: A1
- Status: DRAFT_ONLY

## Contraintes

- READ_ONLY uniquement
- Aucun write durable
- Aucun secret / .env
- Aucun git add/commit/push automatique
- Si un fichier tracke est modifie, BLOCKED_WITH_REASON
