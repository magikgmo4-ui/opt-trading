# 20_LOCAL_VIEW_INPUTS

## Objectif

Definir les inputs autorises du render graph reel local WHY/runtime.

## Inputs candidats

| Input | Usage |
| --- | --- |
| markdown WHY docs | relations WHY/runtime |
| runtime graph docs | dependances runtime |
| governance docs | review humaine |
| static JSON graph | import graph |
| observability metadata | preuves runtime |
| scoring snapshots | contextualisation criticite |

## Inputs interdits

| Input | Raison |
| --- | --- |
| runtime temps reel | hors scope |
| connecteurs live | interdit |
| APIs runtime | interdit |
| CI live | interdit |

## Formats candidats

| Format | Usage |
| --- | --- |
| markdown | review humaine |
| json | graph statique |
| static metadata | overlays runtime |

## Invariant

Les inputs WHY/runtime doivent rester statiques, tracables et lecture seule.
