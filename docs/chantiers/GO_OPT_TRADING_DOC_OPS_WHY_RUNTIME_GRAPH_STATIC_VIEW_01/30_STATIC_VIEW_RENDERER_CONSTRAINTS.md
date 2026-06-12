# 30_STATIC_VIEW_RENDERER_CONSTRAINTS

## Objectif

Definir les contraintes du renderer de la vue statique WHY/runtime.

## Contraintes principales

| Contrainte | Protection |
| --- | --- |
| lecture seule | protection runtime |
| aucun runtime live | isolation runtime |
| aucun connecteur live | protection gouvernance |
| aucun traversal decisionnel | protection critique |
| aucun APPLY runtime | protection execution |
| aucun dashboard live | limitation autonomie |

## Regles renderer

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

Le renderer WHY/runtime doit rester local, explicable et non decisionnel.

## RISKS

- À qualifier.
