---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_PROPOSITION_ENGINE_STRATEGY_ID_ADAPTER_READONLY_01
go_type: child
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
repo: opt-trading
status: open
created_at: 2026-05-18
surface: code / doc
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_PROPOSITION_ENGINE_STRATEGY_ID_ADAPTER_READONLY_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Raccorder `proposition_engine` à `modules.strategy.adapter` en lecture seule, pour valider les `strategy_id` reçus sans modifier la génération de propositions.

### 2_CONTEXTE

- `modules/strategy/adapter.py` opérationnel.
- `trading_realtime_v1` raccordé.
- `signal_router` raccordé.
- `proposition_engine` reçoit `NormalizedSignal.strategy_id` du signal_router et le propage dans le prompt OpenClaw.
- Aucune validation registry n'existe encore ici.

### 3_SCOPE

- Ajouter `validate_strategy_id()` dans `PropositionEngine.propose()`.
- Warning log si inconnu, pas de rejet, pas de modification des propositions.
- Pas de changement de scoring, payload, prompt, ou décision.

### 4_RESUME_POINT

Signal_router terminé. Prochaine étape : proposition_engine.

## RISKS

- À qualifier.
