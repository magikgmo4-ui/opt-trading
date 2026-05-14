# 80_CONVERGENCE_IMPLEMENTATION_ORDER

## Objectif

Definir l'ordre futur des implementations reelles WHY.

## Ordre recommande

| Phase | Surface |
| --- | --- |
| V1 | parser WHY stable |
| V2 | score generator stable |
| V3 | lint governance experimental |
| V4 | runtime graph visualisation |
| V5 | governance dashboard |
| V6 | worker WHY reel |
| V7 | CI governance experimentale |
| V8 | dashboard live |

## Raison

L'ordre doit:
- minimiser les risques runtime,
- maximiser l'explicabilite,
- maintenir review humaine,
- eviter une derive autonome precoce.

## Conditions avant implementation reelle

| Condition | Necessaire |
| --- | --- |
| observabilite stable | oui |
| review humaine stable | oui |
| runtime graph stable | oui |
| governance documentee | oui |
| recovery paths documentes | oui |

## Invariant

Aucune implementation reelle WHY ne doit contourner la governance humaine.
