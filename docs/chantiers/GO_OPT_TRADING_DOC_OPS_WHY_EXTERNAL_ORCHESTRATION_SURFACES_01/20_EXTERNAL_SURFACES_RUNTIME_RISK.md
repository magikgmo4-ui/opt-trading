# 20_EXTERNAL_SURFACES_RUNTIME_RISK

## Objectif

Evaluer les risques runtime des surfaces externes candidates.

## Risques candidats

| Surface | Risque principal |
| --- | --- |
| ClickUp | derive priorisation |
| Botpress | autonomie conversationnelle |
| Knowledge Graph | corruption relationnelle |
| Airtable | derive source de verite |

## Risques transverses

| Risque | Impact |
| --- | --- |
| sync incoherent | divergence runtime |
| source externe obsolete | mauvaises decisions |
| automation prematuree | derive IA |
| observabilite insuffisante | audit incomplet |

## Regles

- Les surfaces externes doivent rester auditables.
- Les surfaces critiques doivent garder review humaine.
- Les donnees externes doivent etre contextualisees.
- Les integrations runtime doivent etre explicites.

## Invariant

Aucune surface externe ne doit devenir une source runtime autonome sans governance WHY explicite.
