# 110_EXTERNAL_SURFACES_REPORTING_ARCHITECTURE

## Objectif

Structurer l'architecture reporting des surfaces externes candidates.

## Sorties candidates

| Sortie | Role |
| --- | --- |
| external_surfaces_report.json | sortie machine-readable |
| external_surfaces_summary.md | synthese humaine |
| external_surfaces_runtime_alignment.md | coherence runtime |
| external_surfaces_review_gates.md | besoins review humaine |

## Niveaux reporting

| Niveau | Usage |
| --- | --- |
| governance | coherence WHY/runtime |
| runtime | surfaces critiques |
| audit | tracabilite |
| human review | validation humaine |

## Observation

Les rapports doivent rester:
- explicables,
- auditables,
- non destructifs,
- lisibles humainement.

## Invariant

Les rapports des surfaces externes ne doivent jamais devenir des validations runtime autonomes.
