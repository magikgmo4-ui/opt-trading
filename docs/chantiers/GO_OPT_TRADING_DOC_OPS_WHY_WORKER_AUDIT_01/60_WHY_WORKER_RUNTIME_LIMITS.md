# 60_WHY_WORKER_RUNTIME_LIMITS

## Objectif

Formaliser les limites runtime du futur worker WHY.

## Limites principales

| Limite | Raison |
| --- | --- |
| aucun APPLY automatique | protection runtime |
| aucun merge automatique | governance humaine |
| aucun FAIL runtime autonome | protection surfaces critiques |
| aucune execution live | audit uniquement |
| aucune correction documentaire | non destructif |

## Surfaces critiques

Les surfaces R4/R5:
- doivent garder review humaine,
- doivent garder preuves runtime,
- ne doivent jamais dependre uniquement du worker WHY.

## Observation

Le worker WHY doit rester:
- documentaire,
- explicable,
- audit-oriented,
- non destructif.

## Invariant

Le worker WHY ne doit jamais devenir une autorite runtime autonome.

## RISKS

- À qualifier.
