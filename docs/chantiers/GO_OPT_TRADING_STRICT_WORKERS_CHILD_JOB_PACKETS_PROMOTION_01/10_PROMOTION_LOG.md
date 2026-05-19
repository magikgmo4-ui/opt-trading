---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_JOB_PACKETS_PROMOTION_01_PROMOTION_LOG
doc_type: promotion_log
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
  - log
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
---

# 10_PROMOTION_LOG

## Conversion mapping

Pour chaque draft, les champs suivants sont convertis du format worker-pool-extension
vers le format strict-workers validable:

| Draft field | Target field | Notes |
|---|---|---|
| job_packet_id | job_packet_id | Identique |
| go_id | go_id | Identique |
| task | task_type | Renommage |
| status | status | Identique |
| model | default_worker | Prefixe opencode/ retire |
| fallback_models | worker_candidates | Fusion + preferred_workers depuis tasks.index.json |
| inputs.allowed | scope.allowed_inputs | Identique |
| output.path | scope.allowed_outputs | Tableau a 1 element |
| output.required_sections | required_output_sections | Identique |
| (nouveau) | instructions | Liste de consignes generees |
| (nouveau) | acceptance | Criteres generes |
| (nouveau) | model_registry | Chemin fixe |
| (nouveau) | task_index | Chemin fixe |
| (nouveau) | scope.denied_inputs_inherited | true |
| autonomy_max, writes_code, denied_commands | (supprime) | Lues depuis tasks.index.json |
| validation, stop_conditions, healthcheck | (supprime) | Non utilise par validateur |

## Fichiers crees

| Fichier | Source draft | task_type |
|---|---|---|
| scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01.json | 40_JOB_PACKET_DRAFTS.md:31 | READ_INVENTORY |
| scripts/ai/workers/job_packets/GO_STRICT_WORKERS_PATCH_DRAFT_MATRIX_01.json | 40_JOB_PACKET_DRAFTS.md:67 | PATCH_DRAFT |
| scripts/ai/workers/job_packets/GO_STRICT_WORKERS_DOC_DRAFT_MATRIX_01.json | 40_JOB_PACKET_DRAFTS.md:101 | DOC_DRAFT |
| scripts/ai/workers/job_packets/GO_STRICT_WORKERS_TESTPLAN_MATRIX_01.json | 40_JOB_PACKET_DRAFTS.md:133 | TESTPLAN |
| scripts/ai/workers/job_packets/GO_STRICT_WORKERS_CHERRY_PICK_INVENTORY_MATRIX_01.json | 40_JOB_PACKET_DRAFTS.md:165 | CHERRY_PICK_INVENTORY |
| scripts/ai/workers/job_packets/GO_STRICT_WORKERS_FAST_TRIAGE_MATRIX_01.json | 40_JOB_PACKET_DRAFTS.md:197 | FAST_TRIAGE |
| scripts/ai/workers/job_packets/GO_STRICT_WORKERS_ENDPOINT_AUDIT_MATRIX_01.json | 40_JOB_PACKET_DRAFTS.md:229 | ENDPOINT_AUDIT |
| scripts/ai/workers/job_packets/GO_STRICT_WORKERS_WRITE_GATED_DRYRUN_MATRIX_01.json | 40_JOB_PACKET_DRAFTS.md:261 | WRITE_GATED |

## Decisions

1. worker_candidates bases sur preferred_workers de tasks.index.json (source of truth)
2. default_worker correspond au modele prefere du draft (prefixe opencode/ retire)
3. allowed_inputs conserves depuis les drafts, avec ajustements pour cherry_pick (git commands -> file globs) et endpoint_audit (URL -> registry)
4. allowed_outputs en chemin exact (<task_type>_MATRIX_01.md) comme les packets existants
5. instructions generees selon le type de tache (read-only, write-gated, etc.)
6. acceptance adaptee par type (dry_run_required pour PATCH_DRAFT et WRITE_GATED, must_not_run_tests pour TESTPLAN, etc.)
