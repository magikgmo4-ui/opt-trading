# 90_WHY_WORKER_STATE_MACHINE

## Objectif

Formaliser la machine d'etats du futur worker d'audit WHY.

## Etats candidats

| Etat | Role |
| --- | --- |
| DISCOVER | trouver les surfaces documentaires cibles |
| LOAD | charger documents et sorties parser/scoring |
| PARSE_ATTACH | rattacher les resultats parser |
| SCORE_ATTACH | rattacher les scores WHY |
| GAP_ANALYZE | analyser les gaps critiques |
| RUNTIME_ALIGN | aligner avec classes R0-R5 |
| MULTI_MACHINE_CHECK | verifier impacts multi-machine |
| REVIEW_CLASSIFY | determiner besoin review humaine |
| REPORT_BUILD | produire rapports audit |
| REVIEW_READY | livrer paquet pret review |
| SKIP | ignorer surface hors scope |
| PARTIAL | analyse incomplete mais exploitable |
| ERROR | echec localise |

## Transitions

| Depuis | Vers | Condition |
| --- | --- | --- |
| DISCOVER | LOAD | documents trouves |
| LOAD | PARSE_ATTACH | sources chargees |
| PARSE_ATTACH | SCORE_ATTACH | sections disponibles |
| SCORE_ATTACH | GAP_ANALYZE | score ou absence score traitee |
| GAP_ANALYZE | RUNTIME_ALIGN | gaps classes |
| RUNTIME_ALIGN | MULTI_MACHINE_CHECK | classe runtime connue ou UNKNOWN |
| MULTI_MACHINE_CHECK | REVIEW_CLASSIFY | dependances evaluees |
| REVIEW_CLASSIFY | REPORT_BUILD | besoins review identifies |
| REPORT_BUILD | REVIEW_READY | rapports produits |
| any | SKIP | surface hors scope |
| any | PARTIAL | donnees incompletes |
| any | ERROR | echec non recuperable localement |

## Invariants

- ERROR ne bloque pas tout le batch.
- PARTIAL doit etre explicite.
- REVIEW_READY ne signifie pas validation runtime.
- Aucun etat ne declenche APPLY.

## RISKS

- À qualifier.
