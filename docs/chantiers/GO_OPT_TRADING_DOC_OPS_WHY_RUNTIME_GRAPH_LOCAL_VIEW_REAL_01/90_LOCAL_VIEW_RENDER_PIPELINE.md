# 90_LOCAL_VIEW_RENDER_PIPELINE

## Objectif

Preparer le pipeline du premier render effectif WHY/runtime local.

## Pipeline candidat

| Etape | Role |
| --- | --- |
| LOAD_SOURCES | charger markdown/JSON statiques |
| EXTRACT_NODES | extraire nodes WHY/runtime |
| EXTRACT_EDGES | extraire relations documentees |
| APPLY_OVERLAYS | appliquer overlays R0-R5/observabilite/review |
| BUILD_LOCAL_VIEW | construire vue locale |
| EXPORT_REVIEW_ARTIFACTS | produire outputs reviewables |

## Contraintes

- Lecture seule.
- Sources statiques uniquement.
- Aucun runtime live.
- Aucun connecteur live.
- Aucun traversal decisionnel.
- Aucun APPLY runtime.

## Outputs attendus

| Output | Usage |
| --- | --- |
| static graph image | review visuelle |
| markdown snapshot | synthese humaine |
| graph JSON draft | export futur |
| overlay report | criticite et preuves |

## Invariant

Le pipeline de render WHY/runtime doit rester local, statique et non decisionnel.

## RISKS

- À qualifier.
