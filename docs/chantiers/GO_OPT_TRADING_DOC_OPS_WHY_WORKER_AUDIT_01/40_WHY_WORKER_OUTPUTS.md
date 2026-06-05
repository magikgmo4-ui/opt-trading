# 40_WHY_WORKER_OUTPUTS

## Objectif

Definir les sorties futures du worker WHY.

## Sorties candidates

| Sortie | Role |
| --- | --- |
| why_worker_report.json | sortie machine-readable |
| why_worker_summary.md | synthese humaine |
| why_worker_gaps.md | gaps critiques |
| why_worker_runtime_alignment.md | coherence runtime |
| why_worker_review_ready.md | preparation review humaine |

## Champs candidats

| Champ | Role |
| --- | --- |
| document_path | source analysee |
| runtime_class | classe R0-R5 |
| score | score WHY |
| gaps | gaps critiques |
| warnings | warnings |
| explainability | justification audit |
| review_required | besoin review humaine |

## Observation

Les sorties doivent rester:
- audit-oriented,
- explicables,
- non destructives,
- lisibles humainement.

## Invariant

Les sorties du worker WHY ne doivent jamais devenir des gates runtime autonomes.

## RISKS

- À qualifier.
