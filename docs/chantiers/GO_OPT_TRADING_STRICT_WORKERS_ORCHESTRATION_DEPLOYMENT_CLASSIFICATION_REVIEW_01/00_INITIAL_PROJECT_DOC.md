---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: strict_workers
go_id: GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01
parent_go_id: GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01
machine: fantome
status: draft_canonical
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - strict_workers
  - orchestration
  - deployment
  - systemd
  - runtime_map
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01/00_classification_matrix.md
point_de_reprise: "Ouvrir le bucket 1 de PR #645 en revue read-only des workflows strict-workers, du deploy systemd et de config/machine_runtime_map.yml"
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01/00_classification_matrix.md
  - .github/workflows/strict-workers-validate.yml
  - .github/workflows/strict-workers-smoke.yml
  - deploy/systemd/opt-trading-fleet-orchestrator.service
  - deploy/systemd/opt-trading-fleet-orchestrator.timer
  - deploy/systemd/opt-trading-runtime-health.service
  - deploy/systemd/opt-trading-runtime-health.timer
  - config/machine_runtime_map.yml
---

# GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Produire une revue doc-first, strictement read-only, du bucket `GO_STRICT_WORKERS_ORCHESTRATION_ET_DEPLOIEMENT` issu de PR #645 afin de borner clairement les surfaces workflows, `systemd` et `machine_runtime_map` avant toute execution ou modification runtime.

## 2_PARENT_HERITAGE

| Heritage | Source |
|----------|--------|
| Reprise post faux repair Git | PR #645: `docs/chantiers/GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01/00_classification_matrix.md` |
| Validation CI strict workers | `.github/workflows/strict-workers-validate.yml` |
| Smoke read-only strict workers | `.github/workflows/strict-workers-smoke.yml` |
| Orchestration deploy fleet/runtime | `deploy/systemd/*` |
| Canon machine/runtime | `config/machine_runtime_map.yml` |

## 3_BORNES_DU_CHILD

1. Inclure uniquement les surfaces suivantes:
   - `.github/workflows/strict-workers-validate.yml`
   - `.github/workflows/strict-workers-smoke.yml`
   - `deploy/systemd/*`
   - `deploy/systemd/overrides/*`
   - `config/machine_runtime_map.yml`
   - `modules/*/systemd/*` comme surfaces adjacentes a inventorier
2. Exclure `strict-workers-schedule.yml`, qui reste dans le bucket 2 planification/job packets.
3. Exclure `strategy`, `airtable_bridge`, `OpenClaw policy`, `OpenClaw DBLayer`, `Botpress`, `Ollama` et tout index global.
4. Ne faire aucun write runtime, aucun changement `systemctl`, aucune activation timer/service.

## 4_SORTIE_ATTENDUE

1. Un inventaire borne des surfaces bucket 1.
2. Une classification par sous-famille:
   - workflows strict-workers read-only
   - unites `systemd` deploy fleet/runtime
   - overrides machine-specifiques
   - carte canonique machine/runtime
   - modules annexes exposes via `systemd`
3. Une liste explicite des surfaces hors scope a renvoyer vers d'autres buckets.

## 5_INVARIANTS

- Travail read-only et doc-first uniquement.
- Aucune modification du runtime reel.
- Aucun changement de contenu hors `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01/`.
- La revue doit rester une etape de classification, pas d'implementation.

## 6_BRANCHE_CIBLE

Branche dediee cible pour une PR ulterieure si necessaire: `go/GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01`.
