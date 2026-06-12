# 80_WHY_SCORE_AUDIT_OUTPUTS

## Objectif

Preparer les futures sorties audit du WHY score generator.

## Sorties candidates

| Sortie | Role |
| --- | --- |
| why_score_report.json | sortie machine-readable |
| why_score_summary.md | synthese humaine |
| why_score_gaps.md | gaps critiques |
| why_runtime_alignment.md | coherence runtime |

## Champs candidats

| Champ | Role |
| --- | --- |
| document_path | source analysee |
| runtime_class | classe R0-R5 |
| detected_sections | sections trouvees |
| missing_sections | sections absentes |
| penalties | penalites |
| warnings | warnings |
| final_score | score WHY |
| explainability | justification score |

## Observation

Les sorties audit doivent rester:
- explicables,
- lisibles,
- non destructives,
- audit-oriented.

## Invariant

Les sorties audit ne doivent jamais devenir une gate runtime autonome.

## RISKS

- À qualifier.
