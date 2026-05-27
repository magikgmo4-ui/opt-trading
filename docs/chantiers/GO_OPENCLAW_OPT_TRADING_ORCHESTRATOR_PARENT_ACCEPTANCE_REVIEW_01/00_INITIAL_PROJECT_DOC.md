---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01
go_structural_role: GO_STANDALONE
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: open
lifecycle_stage: opening
surface: docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01
source_kind: canonical
updated_at: 2026-05-26
topic_keys:
  - openclaw
  - orchestration
  - acceptance-review
  - regression-fix
---

# 00_INITIAL_PROJECT_DOC — Parent Acceptance Review

## 1_MASTER_TARGET

Valider la chaîne produit complète `PF_OPENCLAW_ORCHESTRATOR_FULL` après closeout du parent (2026-05-25) et closeout du learning_feeder (2026-05-26 PR #824). Produire un rapport d'acceptation indépendant. Documenter les gaps comme extensions, pas comme blocages.

## 2_INITIAL_PROJECT_DOC

Cette fiche ouvre `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01`.

## 3_INITIAL_NEED

La revue d'acceptation parent est distincte du closeout (90_PARENT_CLOSEOUT.md déjà en place). Elle inclut :
- Validation de tous les tests en run combiné (pas juste isolés)
- Correction des régressions découvertes
- Inventaire des gaps réels vs extensions planifiées

## 4_SCOPE

- Docs : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01/`
- Bug fix : `modules/notification_dispatcher/app/__init__.py`, `modules/validation_gate/app/gate.py`, `modules/trade_executor/app/executor.py`, `modules/result_tracker/app/tracker.py`

## 5_FINAL_TARGET

- 20_ACCEPTANCE_REVIEW.md produit et PASS
- 126 tests en run combiné → ALL PASS (regression PipelineEvent fixée)
