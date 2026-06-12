# 90_LINT_AUTONOMY_LIMITS

## Objectif

Verrouiller les limites d'autonomie du WHY lint experimental.

## Limites principales

| Limite | Raison |
| --- | --- |
| aucun auto-fix | non destructif |
| aucune CI bloquante | experiment only |
| aucun APPLY automatique | protection runtime |
| aucun merge automatique | governance humaine |
| aucune validation runtime autonome | protection surfaces critiques |
| aucune promotion automatique R0-R5 | anti hallucination |

## Regles

- Le lint lit et signale seulement.
- Le lint ne corrige pas.
- Le lint ne valide pas.
- Le lint ne remplace pas la review humaine.
- Le lint ne doit pas devenir une autorite runtime.

## Surfaces critiques

Les surfaces R4/R5 doivent garder:
- review humaine,
- preuves runtime,
- observabilite,
- recovery path.

## Invariant

Le WHY lint reste warning-only, lecture seule et audit-oriented.

## RISKS

- À qualifier.
