# 100_WHY_PARSER_DOCUMENT_PRIORITY

## Objectif

Definir la priorite documentaire du futur parser WHY.

## Priorites candidates

| Priorite | Surface | Raison |
| --- | --- | --- |
| P0 | governance WHY | doctrine critique |
| P1 | GO runtime R4/R5 | criticite forte |
| P2 | closeouts critiques | reprise et audit |
| P3 | parent docs | coherence produit |
| P4 | docs historiques | faible impact |

## Regles

- Les surfaces P0/P1 doivent etre analysees en premier.
- Les surfaces R4/R5 doivent recevoir des checks plus stricts.
- Les documents historiques peuvent etre analyses en mode best effort.
- Les documents doc-only peuvent tolerer plus de gaps.

## Observation

La priorite documentaire doit suivre:
- criticite runtime,
- impact produit,
- risque de derive,
- besoin de reprise.

## Invariant

Le parser ne doit jamais traiter un document historique comme une source runtime prioritaire sans preuve explicite.

## RISKS

- À qualifier.
