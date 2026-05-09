# 90_WHY_PARSER_STATE_MACHINE

## Objectif

Formaliser les etats et transitions du futur parser WHY.

## Etats candidats

| Etat | Role |
| --- | --- |
| DISCOVER | trouver les fichiers markdown cibles |
| LOAD | lire le contenu brut |
| NORMALIZE | normaliser headings et accents |
| SEGMENT | separer les sections markdown |
| CLASSIFY | classifier les sections WHY |
| VALIDATE | detecter gaps et incoherences |
| SCORE_PREP | preparer les donnees de scoring |
| REPORT | produire une sortie audit |
| SKIP | ignorer surface non cible |
| ERROR | signaler lecture impossible |

## Transitions

| Depuis | Vers | Condition |
| --- | --- | --- |
| DISCOVER | LOAD | fichier cible trouve |
| LOAD | NORMALIZE | contenu lisible |
| NORMALIZE | SEGMENT | headings detectables |
| SEGMENT | CLASSIFY | sections extraites |
| CLASSIFY | VALIDATE | sections classees |
| VALIDATE | SCORE_PREP | gaps calcules |
| SCORE_PREP | REPORT | donnees pretes |
| any | SKIP | surface hors scope |
| any | ERROR | lecture impossible |

## Invariants

- Aucun etat ne modifie le fichier source.
- ERROR ne doit pas interrompre tout le batch.
- SKIP doit etre explicite et journalisable.
- REPORT doit rester audit-only.
