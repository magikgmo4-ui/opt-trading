---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_WORKER_JOB_GRAPH
doc_type: worker_job_graph
repo: opt-trading
project: opt-trading
module: strict_workers
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
status: draft_canonical
lifecycle_stage: opening
surface: chantier
source_kind: canonical
updated_at: 2026-05-22
topic_keys:
  - workers
  - job_graph
  - strict_workers
  - delegation
---

# 30_WORKER_JOB_GRAPH

## 1_OBJECTIF

Definir les jobs delegables pour ce chantier en reutilisant les tasks strict workers deja presentes.

## 2_JOB_GRAPH

| Ordre | job_id | task | autonomie | worker prefere | Gate | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_READ_INVENTORY_01` | `READ_INVENTORY` | A1 | `qwen3.5-plus` ou `deepseek-v4-flash-free` | none | `reports/ai/workers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_READ_INVENTORY_01.md` |
| 02 | `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_FAST_TRIAGE_01` | `FAST_TRIAGE` | A1 | `gpt-5-nano` ou `deepseek-v4-flash-free` | none | `reports/ai/workers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_FAST_TRIAGE_01.md` |
| 03 | `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_PATCH_DRAFT_01` | `PATCH_DRAFT` | A2 | `glm-5.1` ou `kimi-k2.6` | dry_run | `reports/ai/workers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_PATCH_DRAFT_01.md` |
| 04 | `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_TESTPLAN_01` | `TESTPLAN` | A2 | `qwen3.6-plus` ou `glm-5.1` | dry_run | `reports/ai/workers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_TESTPLAN_01.md` |
| 05 | `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_DOC_DRAFT_01` | `DOC_DRAFT` | A2 | `qwen3.5-plus` ou `minimax-m2.7` | dry_run | `reports/ai/workers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_DOC_DRAFT_01.md` |
| 06 | `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_ENDPOINT_AUDIT_01` | `ENDPOINT_AUDIT` | A1 | `qwen3.5-plus` | none | `reports/ai/workers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_ENDPOINT_AUDIT_01.md` |
| 07 | `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_WRITE_GATED_01` | `WRITE_GATED` | A4 | `glm-5.1` ou `qwen3.6-plus` | human_approve + dry_run | `reports/ai/workers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_WRITE_GATED_01.md` |

## 3_DELEGATION_MODEL

### Session forte

- ChatGPT 5.5 Thinking : cadrage, arbitrage, patch final, evaluation target.
- Claude Opus/Sonnet : review critique, coherence docs, checklist humaine.
- GPT 5.5 IDE : application patch, validation locale, tests.

### Strict workers

- A1 : inventaire, triage, audit endpoint.
- A2 : patch draft, doc draft, testplan.
- A4 : write gated seulement avec validation humaine explicite.

## 4_CREATION_DE_NOUVEAUX_JOBS

Creation interdite par defaut. Autorisee seulement si :

- aucune task existante ne couvre le besoin ;
- le gap est documente ;
- la nouvelle task respecte les invariants ;
- le changement est isole dans un GO dedie strict workers.

## 5_EVIDENCE_REF

Chaque job doit produire un rapport sous `reports/ai/workers/` avec les sections requises par `tasks.index.json`.
