---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ENGINE_REGISTRY_ADAPTER_PHASE_01
doc_type: contract
---

# 20_ADAPTER_CONTRACT

## Contrat

`modules/strategy/adapter.py` fournit :

| Fonction | Signature | Rôle |
|----------|----------|------|
| `validate_strategy_id` | `(strategy_id: str) -> bool` | Vérifie si un strategy_id est connu du registry |
| `get_known_ids` | `() -> set[str]` | Retourne tous les strategy_id enregistrés |
| `lookup_strategy` | `(strategy_id: str) -> StrategyRegistryEntry \| None` | Retourne l'entrée registry ou None |

## Dépendances

- `modules/strategy/registry.py` (loader)
- `modules/strategy/types.py` (StrategyRegistryEntry)
- `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md` (source canonique)

## Invariants

- Aucun effet de bord runtime.
- Aucune écriture.
- Aucune modification des engines existants.
- Chargement registry lazy (au premier appel).

## Non-scope

- Migration engines.
- Changement de signaux/routing.
- Exécution trading.
- Backfill registry supplémentaire.
