---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ENGINE_REGISTRY_ADAPTER_PHASE_01
go_type: child
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
repo: opt-trading
status: open
created_at: 2026-05-18
surface: code / doc
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ENGINE_REGISTRY_ADAPTER_PHASE_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Raccorder progressivement les engines existants à `modules/strategy/`, sans changer leur comportement trading.

Phase 1 : ajouter un adapter léger lecture/validation seulement.

### 2_CONTEXTE

- Registry complète : 7 entrées, 0 UNREGISTERED.
- `modules/strategy/` actif comme surface physique canonique minimale : types, loader, contrat.
- Validateur `tools/strategy/validate_strategy_registry.py` opérationnel.
- Aucun engine n'importe `modules/strategy/` actuellement.

### 3_SCOPE

- Créer `modules/strategy/adapter.py` : adapter lecture/validation.
- Ajouter test smoke pour l'adapter.
- Documents : audit surfaces, contrat adapter, décision implémentation, gate, closeout.
- Ne pas modifier le comportement trading runtime.
- Ne pas déplacer les engines.
- Ne pas faire de refactor massif.

### 4_SURFACES AUDITÉES

- `trading_realtime_v1` — hardcode `xau_session_open_v1`
- `trading_lab_v1` — lit strategy_id depuis profil YAML, fallback `xau_session_open_v1`
- `decision_engine` — pas de strategy_id explicite
- `signal_router` — strategy_id dans SignalIn/NormalizedSignal
- `proposition_engine` — pass-through strategy_id
- `notification_dispatcher` — template strategy_id

### 5_RESUME_POINT

Base stratégie complète. Ce GO ajoute une fine couche adapter avant toute migration engine.

## RISKS

- À qualifier.
