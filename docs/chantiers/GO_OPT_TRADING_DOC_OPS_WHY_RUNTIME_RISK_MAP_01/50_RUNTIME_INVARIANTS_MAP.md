# 50_RUNTIME_INVARIANTS_MAP

## Objectif

Documenter les invariants runtime non negociables.

## Invariants critiques

| ID | Invariant | Surface |
| --- | --- | --- |
| RI-01 | etat reel > memoire | toutes |
| RI-02 | separation AUDIT/APPLY obligatoire | runtime critique |
| RI-03 | patch minimal prioritaire | runtime sensible |
| RI-04 | aucune execution live sans gates | R4/R5 |
| RI-05 | reprise obligatoire pour surfaces critiques | R3/R4/R5 |
| RI-06 | machine split respecte | multi-machine |
| RI-07 | preuve runtime obligatoire avant validation | runtime |
| RI-08 | GO local != finalite produit | gouvernance |
| RI-09 | invariants documentes avant automation | WHY governance |
| RI-10 | review humaine obligatoire sur surfaces critiques | R4/R5 |

## Observation

Les invariants servent a bloquer:
- les derives IA,
- les optimisations dangereuses,
- les regressions silencieuses,
- les collisions multi-machine.
