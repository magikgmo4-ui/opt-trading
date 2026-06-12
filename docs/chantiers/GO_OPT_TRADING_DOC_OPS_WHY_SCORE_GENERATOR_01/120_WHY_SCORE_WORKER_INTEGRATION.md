# 120_WHY_SCORE_WORKER_INTEGRATION

## Objectif

Preparer l'integration du score generator avec le futur worker WHY.

## Pipeline candidat

Parser WHY -> Score Generator -> Worker Audit -> Reports

## Roles

| Composant | Role |
| --- | --- |
| Parser WHY | lire sections et gaps |
| Score Generator | calculer score contextualise |
| Worker Audit | produire audit WHY |
| Reports | produire sorties humaines et machine-readable |

## Sorties candidates

| Sortie | But |
| --- | --- |
| why_score_report.json | sortie machine-readable |
| why_score_summary.md | synthese humaine |
| why_runtime_alignment.md | coherence runtime |
| why_gaps.md | gaps critiques |

## Invariants

- Aucun APPLY automatique.
- Aucun merge automatique.
- Aucun FAIL runtime autonome.
- Worker audit uniquement.
- Review humaine obligatoire sur surfaces critiques.

## RISKS

- À qualifier.
