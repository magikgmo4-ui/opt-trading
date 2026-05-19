# 30_WHY_SCORE_PENALTIES

## Objectif

Definir les penalites critiques du futur score WHY.

## Penalites candidates

| Penalite | Impact |
| --- | --- |
| WHY absent sur R4/R5 | critique |
| INVARIANTS absents | critique |
| GATES absents | critique |
| RESUME_POINT absent | important |
| FAILURE_MODE absent | important |
| incoherence runtime/gouvernance | critique |
| review humaine absente sur R4/R5 | critique |
| observabilite absente sur runtime critique | critique |

## Regles candidates

- Une penalite critique peut plafonner le score maximal.
- Les surfaces R0 peuvent tolerer plus de gaps.
- Les surfaces R4/R5 doivent etre strictes.
- Les contradictions documentaires doivent etre penalisees.

## Observation

Le score WHY doit favoriser:
- la coherence,
- la reprise,
- l'explicabilite,
- la protection runtime.

## Invariant

Le score WHY ne doit jamais devenir une gate runtime autonome.
