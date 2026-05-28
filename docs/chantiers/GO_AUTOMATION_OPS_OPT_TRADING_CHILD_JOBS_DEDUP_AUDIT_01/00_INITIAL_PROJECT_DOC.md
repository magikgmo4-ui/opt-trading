---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: automation_ops
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
parent_go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: closed
lifecycle_stage: done
topic_keys:
  - opt-trading
  - automation_ops
  - jobs_dedup
  - draft_packets
  - legacy_scripts
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
links:
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01/30_JOBS_DEDUP_PROTOCOL.md
  - docs/registry/JOBS_REGISTRY.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01/10_DUPLICATE_CANDIDATES.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01/20_CONSUMER_MAP.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01/30_DECISION_TABLE.md
---

# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Qualifier les anomalies B01-B06 du JOBS_REGISTRY en appliquant le protocole `30_JOBS_DEDUP_PROTOCOL.md`.
Aucune suppression sans preuve. Aucune mutation sans décision documentée.

## 7_CANONICAL_STATE

| Anomalie | Classification | Verdict |
|---|---|---|
| B01 tasks.index.json DRAFT_ONLY | FALSE_POSITIVE | FORMALIZE_STATUS |
| B02 22 job_packets DRAFT_ONLY | FALSE_POSITIVE | KEEP / FORMALIZE_SCHEMA |
| B03 orchestration contrat non connecté | FALSE_POSITIVE | KEEP_CANDIDATE |
| B04 signal_processor + oauth sans test | NOT_DEDUP | ADD_TEST (batch dédié) |
| B05 gha_strict_workers_schedule sans test | NOT_DEDUP | ADD_TEST (batch dédié) |
| B06 8 scripts apply_desk_pro_*.sh | LEGACY_REPLACED | DELETE_AFTER_PROOF |

## Résultat clé

B06 est le seul vrai candidat à suppression — preuve : `modules/desk_pro/api/routes.py` contient déjà le toolbox (lignes 299-354). Les 8 scripts sont des one-shot déjà appliqués.

## NEXT_GO

```text
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01
```
Après cleanup B06 documenté dans JOBS_REGISTRY.
