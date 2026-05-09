# 110_WHY_WORKER_REPORTING_ARCHITECTURE

## Objectif

Structurer l'architecture reporting du futur worker WHY.

## Sorties candidates

| Sortie | Role |
| --- | --- |
| why_worker_report.json | sortie machine-readable complete |
| why_worker_summary.md | synthese humaine |
| why_worker_gaps.md | gaps critiques |
| why_worker_runtime_alignment.md | coherence runtime |
| why_worker_review_ready.md | preparation review humaine |

## Niveaux reporting

| Niveau | Usage |
| --- | --- |
| machine-readable | automatisation audit future |
| human-readable | review humaine |
| governance | coherence WHY/runtime |
| runtime | surfaces critiques |

## Observation

Les rapports doivent rester:
- explicables,
- auditables,
- non destructifs,
- lisibles humainement.

## Invariant

Les rapports du worker WHY ne doivent jamais devenir des validations runtime autonomes.
