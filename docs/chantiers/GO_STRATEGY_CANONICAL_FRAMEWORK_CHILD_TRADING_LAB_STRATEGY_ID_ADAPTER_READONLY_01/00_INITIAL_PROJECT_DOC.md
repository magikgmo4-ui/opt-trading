---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_STRATEGY_ID_ADAPTER_READONLY_01
go_type: child
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
repo: opt-trading
status: open
created_at: 2026-05-18
surface: code / doc
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_STRATEGY_ID_ADAPTER_READONLY_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Raccorder `trading_lab_v1` a `modules.strategy.adapter` en lecture seule, sur le `strategy_id` lu depuis YAML et sur le fallback `xau_session_open_v1`.

### 2_CONTEXTE

- `modules/strategy/adapter.py` est operationnel.
- Tous les autres engines cibles sont deja raccordes en warning-only.
- `trading_lab_v1` lit `strategy.strategy_id` depuis `xauusd_dual_stack_v1.profile.yaml`.
- `build_market_event()` applique un fallback `xau_session_open_v1` si le champ est absent.

### 3_SCOPE

- Ajouter `validate_strategy_id()` au point de resolution du `strategy_id`.
- Warning si inconnu, silence si connu.
- Valider egalement le fallback quand il est utilise.
- Aucun changement de resultat lab, de fallback, de YAML, ni de hard-fail.

### 4_RESUME_POINT

Dernier engine du rollout adapter strategie.

## RISKS

- À qualifier.
