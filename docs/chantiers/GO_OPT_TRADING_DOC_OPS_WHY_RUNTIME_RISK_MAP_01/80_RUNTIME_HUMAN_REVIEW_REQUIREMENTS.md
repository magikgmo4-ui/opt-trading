# 80_RUNTIME_HUMAN_REVIEW_REQUIREMENTS

## Objectif

Definir les surfaces necessitant une review humaine obligatoire.

## Review humaine obligatoire

| Surface | Classe | Pourquoi |
| --- | --- | --- |
| webhook TradingView | R4 | impact trading live |
| execution financiere automatique | R5 | impact financier direct |
| orchestration multi-machine critique | R3/R4 | derive globale possible |
| provider routing critique | R3/R4 | risque runtime silencieux |
| automation runtime IA | R4/R5 | derive autonome possible |

## Verification minimale humaine

- verifier invariants,
- verifier failure modes,
- verifier reprise,
- verifier impact multi-machine,
- verifier coherence produit.

## Cas de refus

Une review humaine devrait bloquer:
- runtime non cadre,
- absence de reprise,
- absence d'invariants,
- absence de WHY,
- execution live sans preuves.

## Observation

Les surfaces R4/R5 ne devraient jamais etre entierement autonomes sans gates humaines fortes.
