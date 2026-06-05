---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ENGINE_REGISTRY_ADAPTER_PHASE_01
doc_type: implementation_decision
---

# 30_IMPLEMENTATION_DECISION

## Fichiers créés

| Fichier | Rôle |
|---------|------|
| `modules/strategy/adapter.py` | Adapter lecture/validation registry |
| `modules/strategy/__init__.py` | Mise à jour des exports (adapter) |

## Décisions

1. **Adapter léger** : pas de classe, simples fonctions pures.
2. **Registry path** : pointé vers `95_STRATEGY_REGISTRY.md`, même source que le validateur.
3. **Chargement lazy** : le registry n'est parsé qu'au premier appel, pas à l'import.
4. **Validation** : `validate_strategy_id` retourne `bool` (pas d'exception).
5. **Test** : test smoke unitaire qui vérifie les 7 entrées connues.

## Non-fait

- Aucun engine modifié.
- Aucun runtime changé.
- Aucune migration.

## RISKS

- À qualifier.
