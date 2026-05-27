---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: active
created_at: 2026-05-26
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01

## Objectif

Fermer le gap env documenté dans la revue parent `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01/20_ACCEPTANCE_REVIEW.md` :

> `notification_dispatcher` requires `requests` (non dans venv)

Le but est de rendre la dépendance `requests` explicite, testée, et non ambiguë, sans réintroduire d'import eager cassant.

## Contexte

- PR #830 : régression `PipelineEvent` corrigée — import lazy dans `notification_dispatcher/app/__init__.py`.
- PR #834 : Sheets integration test accepté, 46/46 PASS.
- PR #839 : E2E Dry Run LocalCMS Gate fermé, 51/51 PASS.
- Gap restant : `requests` absent du venv / non vérifié par tests.

## Décision

`requests` est une dépendance runtime légitime pour `notification_dispatcher` via `shared/telegram_notify.py`.

Invariants à maintenir :
- pas d'import eager cassant au package import
- `notification_dispatcher.app.events` reste importable sans `requests`
- les tests dry-run ne dépendent pas d'un réseau externe

## Scope

- Vérifier et documenter `requirements.txt` (dépendance canonique).
- Ajouter `modules/notification_dispatcher/tests/test_import_safety.py`.
- Documenter le gap comme CLOSED.
- PR scope limité.

## Ne pas faire

- Ne pas revenir à un import eager cassant.
- Ne pas faire d'appel HTTP réel dans les tests.
- Ne pas modifier secrets/.env.
- Ne pas modifier LocalCMS, Google Sheets API, ni l'orchestrateur parent.
