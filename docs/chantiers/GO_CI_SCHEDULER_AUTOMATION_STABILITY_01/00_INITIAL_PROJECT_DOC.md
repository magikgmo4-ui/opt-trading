---
doc_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01_INITIAL
doc_type: initial_project_doc
go_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-21
links:
  - .github/workflows/strict-workers-validate.yml
  - .github/workflows/strict-workers-smoke.yml
  - .github/workflows/strict-workers-schedule.yml
  - deploy/systemd/opt-trading-runtime-health.timer
  - deploy/systemd/opt-trading-fleet-orchestrator.timer
---

# GO_CI_SCHEDULER_AUTOMATION_STABILITY_01

## Objectif

Stabiliser CI, scheduler, smoke, retry, status et alerting (GAP_09 du parent).

## Périmètre

- Workflows CI recensés
- Smoke critique (exécutable et vérifiable)
- Scheduler (timers systemd, cron)
- Retry policy (tentatives, backoff, dead-letter)
- Status summary (JSON de santé)
- Failure ingestion (collecte et classification des échecs)
- Alerting (Telegram, journal)

## Preuve concrète pour l'ouverture

- `deploy/systemd/` : 2 timers déployés (runtime-health, fleet-orchestrator) sans retry policy ni dead-letter
- `.github/workflows/strict-workers-*` : 3 workflows existants sans status summary ni alerting

## Livrables

- Smoke critique
- Scheduler documenté
- Retry policy
- Status JSON
- Failure ingestion
- Alerting config
