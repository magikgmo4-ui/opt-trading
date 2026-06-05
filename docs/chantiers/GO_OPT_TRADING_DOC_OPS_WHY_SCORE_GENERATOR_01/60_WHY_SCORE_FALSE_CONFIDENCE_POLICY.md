# 60_WHY_SCORE_FALSE_CONFIDENCE_POLICY

## Objectif

Limiter les faux sentiments de qualite produits par un score WHY.

## Risques principaux

| Risque | Effet |
| --- | --- |
| score eleve mais runtime faux | fausse confiance |
| documentation bien ecrite mais non validee | illusion de maturite |
| score automatique sans review | derive governance |
| score hors contexte runtime | mauvaise priorisation |

## Politique

- Un score WHY ne prouve jamais un runtime valide.
- Un score WHY ne remplace jamais une review humaine.
- Un score WHY doit rester contextualise par R0-R5.
- Les surfaces critiques doivent garder des preuves runtime.

## Cas critiques

| Cas | Action |
| --- | --- |
| score eleve sans observabilite | WARN |
| score eleve sans review humaine | IMPORTANT |
| score eleve sur runtime non prouve | IMPORTANT |
| score faible sur doc historique | INFO |

## Invariant

Le score WHY doit rester un outil d'aide a l'audit et non une autorite autonome.

## RISKS

- À qualifier.
