# 70_WHY_PARSER_RUNTIME_LIMITS

## Objectif

Definir les limites runtime du futur parser WHY.

## Limites principales

| Limite | Raison |
| --- | --- |
| aucun APPLY automatique | protection runtime |
| aucune modification de fichier | parser lecture seule |
| aucun merge automatique | governance humaine |
| aucun FAIL runtime autonome | risque de derive |
| aucune inference produit forte | risque hallucination |

## Limites R4/R5

Les surfaces critiques:
- ne doivent jamais dependre uniquement du parser,
- doivent garder des reviews humaines,
- doivent garder des preuves runtime reelles.

## Observation

Le parser WHY doit rester:
- documentaire,
- explicable,
- non destructif,
- audit-oriented.

## Invariant

Le parser ne doit jamais devenir une autorite autonome de validation runtime.
