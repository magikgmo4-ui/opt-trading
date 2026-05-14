# 30_VISUALIZATION_RENDERING_MODEL

## Objectif

Definir le modele de rendu du WHY runtime graph.

## Elements candidats

| Element | Representation |
| --- | --- |
| node WHY | composant documentaire |
| node runtime | surface runtime |
| node machine | machine runtime |
| node observability | preuve runtime |
| node review | gate humaine |
| edge dependency | dependance runtime |
| edge governance | relation governance |
| edge recovery | relation reprise |

## Overlays candidats

| Overlay | Usage |
| --- | --- |
| R0-R5 | criticite runtime |
| observability | preuves runtime |
| review gates | review humaine |
| warnings | gaps documentaires |
| external surfaces | orchestration externe |

## Formats de rendu candidats

| Format | Usage |
| --- | --- |
| graph statique | prototype initial |
| json graph export | integration future |
| markdown snapshot | review humaine |

## Invariant

Le rendu WHY runtime graph ne doit jamais devenir une orchestration runtime autonome.
