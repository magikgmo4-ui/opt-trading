# 20_STATIC_PROTOTYPE_INPUTS

## Objectif

Definir les inputs autorises du prototype graph statique WHY/runtime.

## Inputs candidats

| Input | Usage |
| --- | --- |
| markdown WHY docs | relations WHY/runtime |
| runtime graph docs | dependances runtime |
| governance docs | gates humaines |
| JSON graph statique | import structures graph |
| observability metadata | preuves runtime |
| scoring snapshots | criticite WHY/runtime |

## Inputs interdits

| Input | Raison |
| --- | --- |
| runtime temps reel | hors scope |
| connecteurs live | interdit |
| CI live | interdit |
| APIs runtime | hors scope |

## Formats candidats

| Format | Usage |
| --- | --- |
| markdown | lecture humaine |
| json | import/export graph |
| static metadata | overlays runtime |

## Invariant

Les inputs WHY/runtime doivent rester statiques, lecture seule et tracables.

## RISKS

- À qualifier.
