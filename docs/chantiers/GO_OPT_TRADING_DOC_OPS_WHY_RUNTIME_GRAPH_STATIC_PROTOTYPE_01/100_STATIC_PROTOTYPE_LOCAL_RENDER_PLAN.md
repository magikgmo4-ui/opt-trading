# 100_STATIC_PROTOTYPE_LOCAL_RENDER_PLAN

## Objectif

Preparer le premier render local du prototype WHY/runtime.

## Pipeline candidat

| Etape | Role |
| --- | --- |
| lire markdown WHY | extraire relations |
| lire JSON statique | importer graph |
| construire nodes/edges | preparer rendu |
| appliquer overlays | contextualiser runtime |
| produire rendu statique | review humaine |

## Formats candidats

| Format | Usage |
| --- | --- |
| image statique | visualisation locale |
| markdown snapshot | review governance |
| json export | integration future |

## Contraintes

- Local seulement.
- Lecture seule.
- Aucun runtime live.
- Aucun connecteur live.
- Aucun APPLY runtime.

## Invariant

Le render local WHY/runtime doit rester audit-oriented et non destructif.
