# 30_LOCAL_EXECUTION_CONSTRAINTS

## Objectif

Definir les contraintes d'execution locale du render WHY/runtime.

## Contraintes principales

| Contrainte | Protection |
| --- | --- |
| lecture seule | protection runtime |
| aucun runtime live | isolation runtime |
| aucun connecteur live | protection governance |
| aucun APPLY runtime | protection execution |
| aucun traversal decisionnel | protection critique |
| aucun dashboard live | limitation autonomie |

## Regles execution

- Le renderer lit seulement.
- Le renderer contextualise seulement.
- Le renderer ne valide pas seul un runtime.
- Le renderer ne modifie aucune source.
- Les surfaces critiques gardent validation humaine.

## Conditions avant render reel

| Condition | Necessaire |
| --- | --- |
| governance stable | oui |
| observabilite stable | oui |
| review humaine stable | oui |
| overlays documentes | oui |

## Invariant

Le render WHY/runtime doit rester local, explicable et non decisionnel.

## RISKS

- À qualifier.
