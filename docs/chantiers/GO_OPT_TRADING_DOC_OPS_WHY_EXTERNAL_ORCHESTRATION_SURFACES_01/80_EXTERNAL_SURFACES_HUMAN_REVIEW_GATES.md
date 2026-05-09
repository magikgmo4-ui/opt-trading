# 80_EXTERNAL_SURFACES_HUMAN_REVIEW_GATES

## Objectif

Definir les gates humaines pour les surfaces externes candidates.

## Gates candidates

| Cas | Gate humaine |
| --- | --- |
| propagation statut critique | obligatoire |
| orchestration multi-machine | obligatoire |
| changement governance | obligatoire |
| synchronisation critique | obligatoire |
| source runtime ambigue | obligatoire |

## Politique

Les surfaces externes:
- peuvent assister,
- peuvent contextualiser,
- peuvent structurer,
- peuvent signaler.

Elles ne doivent pas:
- valider seules,
- orchestrer seules,
- merger seules,
- executer seules.

## Observation

Les surfaces externes critiques doivent rester:
- explicables,
- auditables,
- reviewables humainement.

## Invariant

La decision finale doit toujours rester sous gouvernance humaine.
