# 40_WHY_SCORE_RUNTIME_RELATION

## Objectif

Relier le futur score WHY aux classes runtime R0-R5.

## Relation candidate

| Classe | Exigence WHY |
| --- | --- |
| R0 | faible |
| R1 | recommandee |
| R2 | moderee |
| R3 | forte |
| R4 | critique |
| R5 | maximale |

## Effets candidats

| Classe | Effet sur score |
| --- | --- |
| R0 | gaps toleres |
| R1 | faible penalisation |
| R2 | score plus strict |
| R3 | forte importance invariants |
| R4 | review humaine obligatoire |
| R5 | governance complete obligatoire |

## Observation

Le meme score WHY ne doit pas etre interprete de la meme facon selon la criticite runtime.

## Exemple

| Cas | Interpretation |
| --- | --- |
| score 60 sur R0 | acceptable |
| score 60 sur R5 | insuffisant |

## Invariant

Le score WHY doit toujours etre contextualise par la criticite runtime.

## RISKS

- À qualifier.
