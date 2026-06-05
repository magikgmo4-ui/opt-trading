# 30_IA_ORIENTED_WHY_ARCHITECTURE

## Objectif

Transformer le WHY implicite du repo en couche cognitive exploitable par humains et agents IA.

## Architecture cible

| Couche | Role |
| --- | --- |
| WHAT | action demandee |
| HOW | implementation |
| WHY | raison structurelle |
| INVARIANT | ce qui ne doit pas casser |
| FAILURE_MODE | derive historique connue |
| TRADEOFF | compromis accepte |
| GATE | validation obligatoire |

## Principe

Une IA ne doit pas seulement savoir:
- quoi faire,
- comment faire,

mais:
- pourquoi le systeme existe,
- pourquoi certaines limites existent,
- pourquoi certaines optimisations sont interdites.

## Exemple

### Mauvaise approche

"Fusionner tous les collectors dans un schema unique."

### Bonne approche

Comprendre:
- pourquoi les schemas divergent,
- quels consommateurs dependent des variations,
- quels risques existent,
- pourquoi la doctrine interdit le faux-uniformisme.

## Direction future

Creer eventuellement:
- SYSTEM_WHY_LAYER_01.md
- WHY templates standardises
- FAILURE_MODE registry
- TRADEOFF registry
- lecture IA prioritaire WHY avant APPLY

## RISKS

- À qualifier.
