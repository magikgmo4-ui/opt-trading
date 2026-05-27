# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_REGISTRY_CLOSE_GATE_01

## Objectif

Fermer le close gate documentaire et testable du registre stratégie canonique rattaché à `PF_STRATEGY_FRAMEWORK_REGISTRY`. Valider la cohérence entre le registre `95_STRATEGY_REGISTRY.md` et l'adaptateur runtime `modules/strategy/adapter.py`, et corriger le drift des constantes de test.

## Parent

`GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01`

## Périmètre

- Audit de `95_STRATEGY_REGISTRY.md` (IDs, versions, lifecycle, docs_path)
- Audit de la cohérence registry ↔ adapter ↔ tests
- Correction du drift `KNOWN_IDS` dans `tests/test_strategy_adapter.py`
- Décision lifecycle/promotion/retrait pour chaque entrée
- Aucun changement runtime, aucune nouvelle stratégie

## Invariants

- Aucune stratégie ajoutée au registry
- Aucun refactor runtime
- `validate_strategy_id()` comportement inchangé
- Les 4 failures pré-existantes sont causées par le drift test — ce GO les résout

## Issue parent

`PF_STRATEGY_FRAMEWORK_REGISTRY` → `TBD_CLOSE_GATE`
