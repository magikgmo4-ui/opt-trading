# 30_STATIC_PROTOTYPE_RENDERING

## Objectif

Definir le moteur de rendu du prototype graph statique WHY/runtime.

## Elements candidats

| Element | Representation |
| --- | --- |
| WHY node | composant WHY |
| runtime node | surface runtime |
| machine node | machine runtime |
| observability node | preuve runtime |
| review node | gate humaine |
| dependency edge | relation runtime |
| governance edge | relation governance |
| recovery edge | reprise runtime |

## Modes de rendu candidats

| Mode | Usage |
| --- | --- |
| static graph render | vue principale |
| markdown snapshot | review humaine |
| json graph export | integration future |

## Overlays candidats

| Overlay | Usage |
| --- | --- |
| R0-R5 | criticite runtime |
| observability | preuves runtime |
| review gates | validation humaine |
| machine ownership | multi-machine |

## Invariant

Le rendu WHY/runtime doit rester statique, explicable et non decisionnel.
