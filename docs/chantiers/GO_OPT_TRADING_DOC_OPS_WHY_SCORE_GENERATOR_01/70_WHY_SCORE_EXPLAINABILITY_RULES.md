# 70_WHY_SCORE_EXPLAINABILITY_RULES

## Objectif

Rendre le futur score WHY explicable et audit-friendly.

## Regles principales

- Chaque score doit etre decomposable.
- Chaque penalite doit etre explicable.
- Chaque warning doit etre rattache a une section.
- Le score doit indiquer ses limites.

## Sortie explicable candidate

| Champ | Role |
| --- | --- |
| detected_sections | sections trouvees |
| missing_sections | sections absentes |
| penalties | penalites appliquees |
| warnings | gaps mineurs |
| runtime_class | contexte R0-R5 |
| final_score | score global |
| confidence_level | confiance du calcul |

## Observation

Un score non explicable devient:
- difficile a auditer,
- difficile a corriger,
- dangereux pour l'automatisation.

## Invariant

Le score WHY doit toujours pouvoir etre explique a un humain sans logique cachee.

## RISKS

- À qualifier.
