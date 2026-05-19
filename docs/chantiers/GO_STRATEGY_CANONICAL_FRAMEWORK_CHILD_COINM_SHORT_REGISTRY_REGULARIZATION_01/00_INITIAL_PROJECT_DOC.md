---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGISTRY_REGULARIZATION_01
go_type: child
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
repo: opt-trading
status: open
created_at: 2026-05-18
surface: doc-only / registry-only
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGISTRY_REGULARIZATION_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Promouvoir `COINM_SHORT` de `STRATEGY_CANDIDATE P0` (issu du backfill discovery PR #540)
vers `strategy_id` officiel registré, avec spec minimale, surfaces runtime auditées,
gates et limites documentées.

### 2_CONTEXTE

- PR #536 : `SMC_ICT_CHOCH_BOS_RETEST` registrée (entrée #1).
- PR #538 : `xau_session_open_v1` registrée (entrée #2, ACTIVE).
- PR #539 : validateur `validate_strategy_registry.py` opérationnel (WARNING_ONLY).
- PR #540 : backfill discovery mergé ; COINM_SHORT = candidat P0 recommandé.

### 3_SCOPE

Inclus :
- Audit exhaustif des références COINM_SHORT dans le codebase.
- Spec minimale documentée.
- Entrée registry dans `95_STRATEGY_REGISTRY.md`.
- Validation avec `validate_strategy_registry.py`.
- Commit + PR vers `sot/mainline`.

Exclu :
- Pas de création `modules/strategy/`.
- Pas de refactor `strategy_logic.py`.
- Pas de changement runtime trading.
- Pas de promotion des 4 autres candidats (USDTM_LONG, GOLD_CFD_LONG, range_strategy_v1, btc_coinm_accumulation).

### 4_ANCHORED_MEMORY

- `[STRATEGY_BACKFILL_DISCOVERY_MERGED]` : PR #540 mergée (a72dcfc1) ; backfill discovery terminé.
- `[COINM_SHORT_P0_CANDIDATE]` : COINM_SHORT identifié comme candidat P0 avec code engine actif dans `strategy_logic.py` et surface runtime multiple.
- `[MODULES_STRATEGY_DEFERRED]` : modules/strategy/ différé jusqu'à régularisation suffisante du backfill registry.
