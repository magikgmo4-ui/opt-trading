# 90_RUNTIME_GOVERNANCE_MATRIX

## Objectif

Relier criticite runtime, gouvernance WHY, observabilite et orchestration.

## Matrice runtime

| Classe | Gates | Review humaine | Observabilite | Reprise |
| --- | --- | --- | --- | --- |
| R0 | minimale | non | optionnelle | recommandee |
| R1 | WHY recommande | non | faible | recommandee |
| R2 | PASS/FAIL | optionnelle | obligatoire | obligatoire |
| R3 | gates fortes | oui | forte | obligatoire |
| R4 | review obligatoire | forte | critique | obligatoire |
| R5 | governance maximale | obligatoire | critique + supervision | obligatoire |

## Relation WHY

Plus une surface monte en criticite:
- plus le WHY doit etre explicite,
- plus les invariants doivent etre forts,
- plus les gates humaines deviennent importantes.

## Invariant

Aucune surface R4/R5 ne devrait etre pilotee sans:
- observabilite,
- reprise,
- gates,
- review humaine.
