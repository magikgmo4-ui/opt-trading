---
doc_id: GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01_INBOX
doc_type: inbox
repo: opt-trading
project: opt-trading
go_id: GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: impl
surface: index
source_kind: canonical
created_at: 2026-05-21
links:
  - docs/chantiers/GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01/10_SCOPE.md
---

# GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01

## Objet

Runner read-only isolé pour les strict workers (GAP_02 du parent automation gaps).

## Preuve d'ouverture

- `deploy/systemd/*` : services/timers déployés sans runner verrouillé
- `scripts/ai/workers/*` : job packets, tasks index, models registry existent en DRAFT_ONLY

## Prochaine étape

Créer le runner read-only, valider les job packets, exécuter le smoke.
