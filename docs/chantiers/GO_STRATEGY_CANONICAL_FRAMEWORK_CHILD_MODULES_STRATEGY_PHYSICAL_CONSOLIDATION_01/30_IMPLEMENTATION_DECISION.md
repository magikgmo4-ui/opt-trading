---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_MODULES_STRATEGY_PHYSICAL_CONSOLIDATION_01
doc_type: implementation_decision
---

# 30_IMPLEMENTATION_DECISION

## Fichiers créés

| Fichier | Rôle |
|---------|------|
| `modules/strategy/README.md` | Contrat de la couche |
| `modules/strategy/__init__.py` | Exports propres |
| `modules/strategy/types.py` | Types simples |
| `modules/strategy/registry.py` | Loader registry |

## Raccord validateur

Le validateur `tools/strategy/validate_strategy_registry.py` existe déjà et fonctionne
indépendamment. Il n'est pas modifié dans ce GO. La nouvelle couche peut être utilisée
par le validateur dans un GO futur si nécessaire.
