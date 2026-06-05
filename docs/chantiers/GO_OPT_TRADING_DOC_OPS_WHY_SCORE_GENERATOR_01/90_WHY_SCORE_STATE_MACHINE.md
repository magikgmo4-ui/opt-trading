# 90_WHY_SCORE_STATE_MACHINE

## Objectif

Formaliser le pipeline du futur WHY score generator.

## Etats candidats

| Etat | Role |
| --- | --- |
| DISCOVER | identifier les documents cibles |
| LOAD | charger les sorties parser |
| NORMALIZE | normaliser sections et classes |
| SCORE_BASE | calculer score brut |
| APPLY_WEIGHTS | appliquer ponderations |
| APPLY_PENALTIES | appliquer penalites |
| VALIDATE_CONTEXT | verifier runtime class et contexte |
| EXPLAIN | produire justification |
| REPORT | produire sorties audit |
| SKIP | ignorer surface non cible |
| ERROR | signaler impossibilite de score |

## Transitions

| Depuis | Vers | Condition |
| --- | --- | --- |
| DISCOVER | LOAD | document cible trouve |
| LOAD | NORMALIZE | donnees parser disponibles |
| NORMALIZE | SCORE_BASE | sections normalisees |
| SCORE_BASE | APPLY_WEIGHTS | score brut calcule |
| APPLY_WEIGHTS | APPLY_PENALTIES | ponderations appliquees |
| APPLY_PENALTIES | VALIDATE_CONTEXT | penalites appliquees |
| VALIDATE_CONTEXT | EXPLAIN | contexte coherent |
| EXPLAIN | REPORT | justification disponible |
| any | SKIP | surface hors scope |
| any | ERROR | donnees insuffisantes |

## Invariants

- Le score reste indicatif.
- ERROR ne doit pas bloquer tout le batch.
- SKIP doit etre explicite.
- REPORT reste audit-only.
- Aucun etat ne declenche APPLY.

## RISKS

- À qualifier.
