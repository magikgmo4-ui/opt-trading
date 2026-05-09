# 100_WHY_WORKER_RUNTIME_ALIGNMENT

## Objectif

Relier le worker WHY a la governance runtime.

## Alignements critiques

| Classe | Politique worker |
| --- | --- |
| R0 | audit informatif |
| R1 | audit faible criticite |
| R2 | audit contextualise |
| R3 | audit avec invariants forts |
| R4 | review humaine obligatoire |
| R5 | governance maximale obligatoire |

## Regles candidates

| Cas | Action worker |
| --- | --- |
| observabilite absente | signaler critique |
| review humaine absente | signaler critique |
| reprise absente | signaler important |
| runtime UNKNOWN | mode PARTIAL |
| incoherence governance | rapport prioritaire |

## Observation

Le worker WHY doit renforcer:
- l'explicabilite,
- la reprise,
- les invariants,
- la governance runtime.

## Invariant

Le worker WHY ne doit jamais devenir une gate runtime autonome.
