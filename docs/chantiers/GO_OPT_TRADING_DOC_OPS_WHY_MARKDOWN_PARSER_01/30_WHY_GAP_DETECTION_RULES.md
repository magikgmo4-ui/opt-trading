# 30_WHY_GAP_DETECTION_RULES

## Objectif

Definir les gaps critiques detectables par le futur parser WHY.

## Gaps critiques

| ID | Gap | Niveau |
| --- | --- | --- |
| WG-01 | WHY absent sur GO critique | critique |
| WG-02 | INVARIANTS absents sur runtime R3+ | critique |
| WG-03 | RESUME_POINT absent | important |
| WG-04 | FAILURE_MODE absent sur runtime sensible | important |
| WG-05 | FINAL_TARGET absent | mineur |
| WG-06 | GATE absent sur runtime critique | critique |
| WG-07 | incoherence risque vs governance | critique |
| WG-08 | sections contradictoires | important |

## Regles

- Un gap ne doit pas automatiquement devenir un FAIL runtime.
- Les surfaces R0 peuvent tolerer plus de gaps.
- Les surfaces R4/R5 doivent etre strictes.
- Les contradictions detectees doivent etre signalees mais pas corrigees automatiquement.

## Sorties candidates

| Sortie | Sens |
| --- | --- |
| INFO | observation faible |
| WARN | gap mineur |
| IMPORTANT | gap significatif |
| CRITICAL | gap dangereux |

## Invariant

Le parser detecte et signale. Il ne corrige jamais automatiquement.

## RISKS

- À qualifier.
