# 40_WHY_SCORING_PREPARATION

## Objectif

Preparer le futur scoring WHY automatique sans activer de scoring reel.

## Axes de score

| Axe | Score |
| --- | --- |
| WHY explicite | /10 |
| INVARIANTS presents | /10 |
| FAILURE_MODES presents | /10 |
| GATES presents | /10 |
| RESUME_POINT present | /10 |
| CANONICAL_STATE present | /10 |
| coherence runtime/gouvernance | /10 |
| classification R0-R5 coherente | /10 |
| observabilite documentee | /10 |
| reprise documentee | /10 |

## Niveaux candidats

| Score | Niveau |
| --- | --- |
| 0-20 | procedural only |
| 21-40 | WHY faible |
| 41-60 | WHY acceptable |
| 61-80 | WHY solide |
| 81-100 | WHY IA-oriented mature |

## Regles

- Le score ne remplace jamais une review humaine.
- Les surfaces R4/R5 doivent avoir des exigences plus fortes.
- Le score doit rester explicable.
- Un score eleve ne prouve pas la validite runtime.

## Direction future

Le score pourra plus tard:
- alimenter un dashboard governance,
- alimenter un worker audit,
- alimenter une CI experimentale non destructive.

## Invariant

Aucun scoring automatique actif n'est introduit par ce document.
