# 60_WHY_PARSER_FALSE_POSITIVE_POLICY

## Objectif

Reduire les faux positifs du futur parser WHY.

## Sources classiques de faux positifs

| Source | Risque |
| --- | --- |
| texte libre contenant WHY | detection abusive |
| blocs code | fausse section |
| tableaux markdown | confusion structure |
| citations historiques | faux heading |
| aliases ambigus | mauvaise classification |

## Politique

- Favoriser les headings markdown reels.
- Refuser les heuristiques trop agressives.
- Preferer un faux negatif leger a un faux positif critique.
- Les sections detectees doivent rester explicables.

## Cas critiques

| Cas | Action |
| --- | --- |
| heading ambigu | WARN |
| alias inconnu | INFO |
| section contradictoire | IMPORTANT |
| structure malformee | WARN |

## Invariant

Le parser doit rester audit-oriented et non auto-correctif.

## RISKS

- À qualifier.
