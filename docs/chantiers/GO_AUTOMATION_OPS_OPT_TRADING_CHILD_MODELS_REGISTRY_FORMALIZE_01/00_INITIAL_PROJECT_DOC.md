---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_MODELS_REGISTRY_FORMALIZE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
module: ai_workers
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_MODELS_REGISTRY_FORMALIZE_01
status: closed
lifecycle_stage: done
created_at: 2026-05-28
closed_at: 2026-05-28
pr: pending
parent_decision: D4 — SEMIAUTO_JOBS_REGISTRY_PILOT_02 run_report (décision différée, maintenant actée)
links:
  - scripts/ai/workers/models.registry.json
  - tests/test_models_registry.py
  - docs/registry/JOBS_REGISTRY.md
---

# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_MODELS_REGISTRY_FORMALIZE_01

## Objectif

Formaliser `ai_models_registry` (models.registry.json), entré au registre en `experimental` avec
`schema_version: "0.2-draft"`. Ce GO court résout la décision D4 du run SEMIAUTO_JOBS_REGISTRY_PILOT_02
(D4 avait été posé NON, maintenant acté).

Actions :
1. Bump `schema_version` "0.2-draft" → "1.0"
2. Écrire `tests/test_models_registry.py` — validation structure complète
3. Promouvoir `ai_models_registry` : `experimental` → `candidate` dans JOBS_REGISTRY.md v1.6

## Livrable

`tests/test_models_registry.py` — 23 tests, 4 classes :

- `TestRegistryFile` (6) — file exists, valid JSON, schema_version stable (no "draft"), required top-level keys, models dict, non-empty
- `TestModelEntries` (6) — tous les modèles ont status valide, autonomy_max valide, roles liste, roles dans le set connu
- `TestModelConsistency` (7) — VERIFIED → config_id non-null, roles non-vides, autonomy A1/A2 ; INACTIVE → A0, roles vides ; au moins 1 VERIFIED et 1 VERIFIED_FREE
- `TestModelCounts` (4) — VERIFIED ≥8, FREE ≥2, RETIRED ≥2, total 15-100

## État registre après GO

| champ | avant | après |
|-------|-------|-------|
| schema_version | "0.2-draft" | "1.0" |
| JOBS_REGISTRY status | experimental | candidate |
| tests | — | tests/test_models_registry.py (23) |
| next_action | formalize | keep |

## Verdict

```
23/23 PASS
JOBS_REGISTRY.md v1.6 mis à jour :
  ai_models_registry : experimental → candidate
  schema_version     : "0.2-draft" → "1.0"
```
