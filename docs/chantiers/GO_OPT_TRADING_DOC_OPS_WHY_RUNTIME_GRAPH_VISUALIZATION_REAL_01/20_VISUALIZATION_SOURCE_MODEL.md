# 20_VISUALIZATION_SOURCE_MODEL

## Objectif

Definir les donnees sources autorisees pour la visualisation WHY runtime graph.

## Sources autorisees

| Source | Usage |
| --- | --- |
| docs/chantiers | relations WHY |
| runtime graph docs | relations runtime |
| governance docs | gates humaines |
| parser reports | sections et gaps |
| score reports | maturite WHY |
| lint reports | warnings |
| observability metadata | preuves runtime |

## Sources interdites dans cette phase

| Source | Raison |
| --- | --- |
| connecteurs live | hors scope |
| runtime temps reel | non stabilise |
| APPLY runtime | interdit |
| CI live | hors scope |

## Formats candidats

| Format | Usage |
| --- | --- |
| markdown | synthese humaine |
| json | graph export |
| graph metadata | relations runtime |

## Invariant

Les donnees de visualisation doivent rester lecture seule et tracables.

## RISKS

- À qualifier.
