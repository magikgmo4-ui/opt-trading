# 10_WHY_SCORE_MODEL

## Objectif

Definir le modele conceptuel du futur WHY score generator.

## Score global

Le score WHY est un score indicatif de maturite documentaire.

Il ne remplace jamais:
- une review humaine,
- une preuve runtime,
- une validation produit,
- une gate PASS/FAIL.

## Composantes candidates

| Composante | Role | Score |
| --- | --- | --- |
| WHY explicite | raison structurelle | /10 |
| INVARIANTS | limites non negociables | /10 |
| FAILURE_MODES | risques connus | /10 |
| TRADEOFFS | compromis documentes | /10 |
| GATES | validations obligatoires | /10 |
| RESUME_POINT | reprise operationnelle | /10 |
| CANONICAL_STATE | etat valide courant | /10 |
| RUNTIME_CLASS | coherence R0-R5 | /10 |
| OBSERVABILITY | preuves runtime/documentaires | /10 |
| HUMAN_REVIEW | review humaine si critique | /10 |

## Niveaux candidats

| Score | Niveau |
| --- | --- |
| 0-20 | procedural only |
| 21-40 | WHY faible |
| 41-60 | WHY acceptable |
| 61-80 | WHY solide |
| 81-100 | WHY IA-oriented mature |

## Invariant

Un score eleve ne prouve pas que le runtime est valide.
