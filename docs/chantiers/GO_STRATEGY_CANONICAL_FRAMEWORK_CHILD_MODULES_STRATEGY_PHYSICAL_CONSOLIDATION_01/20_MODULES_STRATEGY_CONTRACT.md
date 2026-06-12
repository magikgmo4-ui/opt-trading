---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_MODULES_STRATEGY_PHYSICAL_CONSOLIDATION_01
doc_type: contract
---

# 20_MODULES_STRATEGY_CONTRACT

## Contrat

`modules/strategy/` fournit :

- types stratégie minimaux (`StrategyRegistryEntry`);
- loader registry (`load_strategy_registry`);
- point d'import stable (`from modules.strategy import ...`);
- aucune logique trading.

## Non-scope

- migration engines;
- exécution runtime;
- scoring;
- routing;
- activation stratégie.

## RISKS

- À qualifier.
