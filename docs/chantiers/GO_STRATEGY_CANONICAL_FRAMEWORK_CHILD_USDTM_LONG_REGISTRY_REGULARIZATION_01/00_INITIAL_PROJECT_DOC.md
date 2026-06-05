---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_USDTM_LONG_REGISTRY_REGULARIZATION_01
go_type: child
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
repo: opt-trading
status: open
created_at: 2026-05-18
surface: doc-only / registry-only
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_USDTM_LONG_REGISTRY_REGULARIZATION_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Promouvoir `USDTM_LONG` de `STRATEGY_CANDIDATE P1` (issu du backfill discovery PR #540)
vers `strategy_id` officiel registré, après COINM_SHORT (PR #541).

### 2_CONTEXTE

- PR #540 : backfill discovery mergé ; USDTM_LONG = candidat P1.
- PR #541 : COINM_SHORT registré (entrée #3).
- USDTM_LONG partage le même code engine (`strategy_logic.py`) que COINM_SHORT.

### 3_SCOPE

Inclus : audit surfaces runtime, spec minimale, entrée registry, validation.
Exclu : pas de refactor, pas de changement runtime, pas de modules/strategy/.

### 4_ANCHORED_MEMORY

- `[COINM_SHORT_REGISTERED]` : PR #541 mergée ; COINM_SHORT = entrée #3.
- `[USDTM_LONG_P1_CANDIDATE]` : USDTM_LONG = candidat P1, même pattern.

## RISKS

- À qualifier.
