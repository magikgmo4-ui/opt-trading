---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_REGISTRY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: automation_ops
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_REGISTRY_01
parent_go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: closed
lifecycle_stage: done
topic_keys:
  - opt-trading
  - automation_ops
  - jobs_registry
  - github_actions
  - ai_workers
  - openclaw
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_REGISTRY_01
links:
  - docs/registry/JOBS_REGISTRY.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01/20_JOBS_REGISTRY_SPEC.md
---

# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_REGISTRY_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Construire `docs/registry/JOBS_REGISTRY.md` selon le schéma `20_JOBS_REGISTRY_SPEC.md`.
Aucune mutation de job ou workflow.

## 6_FINAL_TARGET

Registre v1 produit avec ~78 entrées en 6 sections.

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| Registre créé | `docs/registry/JOBS_REGISTRY.md` |
| Sections | 6 (GHA, entry points, job_packets agrégé, workers Python, OpenClaw, scripts racine) |
| Entrées totales v1 | ~78 |
| Anomalies identifiées | B01-B06 |
| Mutation code | aucune |
| Verdict | PASS_JOBS_REGISTRY_V1 |

## Anomalies B01-B06

| ID | Description | Next GO |
|---|---|---|
| B01 | tasks.index.json DRAFT_ONLY | JOBS_DEDUP_AUDIT_01 |
| B02 | 22 job_packets DRAFT_ONLY | JOBS_DEDUP_AUDIT_01 |
| B03 | orchestration contrat non connecté | JOBS_DEDUP_AUDIT_01 |
| B04 | signal_processor + oauth_scope_audit sans test | ADD_TEST batch |
| B05 | gha_strict_workers_schedule sans test | ADD_TEST batch |
| B06 | 6 scripts apply_desk_pro non registrés | JOBS_DEDUP_AUDIT_01 |

## NEXT_GO

```text
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
```
