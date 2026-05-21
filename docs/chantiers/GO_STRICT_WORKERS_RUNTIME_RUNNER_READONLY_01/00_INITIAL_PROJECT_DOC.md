---
doc_id: GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
point_de_reprise: "RUNNER_DRAFT"
created_at: 2026-05-21
links:
  - scripts/ai/workers/run_task.sh
  - scripts/ai/workers/_validate_job.py
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
  - scripts/ai/workers/job_packets/
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - .github/workflows/strict-workers-validate.yml
  - .github/workflows/strict-workers-smoke.yml
  - .github/workflows/strict-workers-schedule.yml
  - deploy/systemd/opt-trading-fleet-orchestrator.service
  - deploy/systemd/opt-trading-runtime-health.service
---

# GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01

## Objectif

Promouvoir les strict workers du statut `DRAFT_ONLY` à un runner read-only réel et verrouillé (GAP_02 du parent).

## Périmètre

- Créer un runner read-only isolé
- Parser et valider les job packets
- Appliquer le no-write guard permanent
- Émettre une sortie JSON normalisée
- Logger par job
- Exécuter un smoke réel
- Garder PATCH_DRAFT hors scope

## Preuve concrète pour l'ouverture

- `deploy/systemd/*` : 2 services (fleet-orchestrator, runtime-health) et leurs timers sont déployés sans runner verrouillé
- `scripts/ai/workers/*` : 3 workflows existent (validate, smoke, schedule) sans runner read-only isolé
- Le socle strict workers est documenté en DRAFT_ONLY mais pas promu runtime

## Livrables

- Runner read-only (script ou module)
- Job packet parser validé
- No-write guard testé
- Sortie JSON normalisée
- Logs par job
- Smoke re-exécutable
- Preuve documentée

## Exclusions

- PATCH_DRAFT (hors scope, GO suivant)
- WRITE_GATED (hors scope)
- Runtime machine-side systemctl (ne pas toucher)
- Aucune modification des workflows CI existants sauf si nécessaire au runner
