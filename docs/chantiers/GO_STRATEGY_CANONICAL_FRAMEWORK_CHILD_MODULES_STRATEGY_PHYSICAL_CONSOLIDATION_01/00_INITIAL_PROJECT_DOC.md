---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_MODULES_STRATEGY_PHYSICAL_CONSOLIDATION_01
go_type: child
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
repo: opt-trading
status: local_prep_only
created_at: 2026-05-18
surface: code / doc
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_MODULES_STRATEGY_PHYSICAL_CONSOLIDATION_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Créer `modules/strategy/` comme surface physique canonique minimale pour les stratégies registrées.

### 2_CONTEXTE

- PR #541-543 : 5 candidats backfill regularisés.
- PR #545 : macro/sector/stat checkup terminé (0 entrée ajoutée).
- Registry : 7 entrées, 0 UNREGISTERED.
- Il manque une surface Python stable pour centraliser types et lecture registry.

### 3_SCOPE

Créer `modules/strategy/` avec types minimaux, loader registry, contrat.
Ne pas refactor runtime, ne pas migrer engines, ne pas ajouter de stratégie.

### 4_RESUME_POINT

Préparation locale sur worktree basé PR #545. Commit après merge #545.

## RISKS

- À qualifier.
