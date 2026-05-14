# 110_CONVERGENCE_DYNAMIC_SCORING_MODEL

## Objectif

Preparer un futur scoring dynamique WHY/runtime convergent.

## Sources candidates

| Source | Usage scoring |
| --- | --- |
| parser WHY | sections et gaps |
| score generator | maturite WHY |
| runtime graph | criticite relations |
| lint experiment | warnings |
| observabilite | preuves runtime |
| human review | validation governance |

## Facteurs candidats

| Facteur | Impact |
| --- | --- |
| WHY complet | score positif |
| review humaine validee | score positif |
| observabilite stable | score positif |
| recovery path documente | score positif |
| gaps critiques | penalite |
| surfaces R5 sans review | penalite critique |

## Regles

- Le scoring doit rester explicable.
- Les penalites doivent etre contextualisees.
- Les surfaces critiques doivent garder review humaine.
- Les scores ne doivent jamais valider seuls un runtime.

## Invariant

Le scoring WHY/runtime ne doit jamais devenir une autorite runtime autonome.
