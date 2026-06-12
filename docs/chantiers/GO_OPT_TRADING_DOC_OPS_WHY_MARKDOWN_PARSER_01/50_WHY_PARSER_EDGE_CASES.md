# 50_WHY_PARSER_EDGE_CASES

## Objectif

Formaliser les cas limites markdown que le futur parser WHY devra gerer.

## Cas limites principaux

| ID | Cas limite | Politique |
| --- | --- | --- |
| EC-01 | heading WHY dans un bloc code | ignorer |
| EC-02 | WHY mentionne dans une phrase | ne pas detecter comme section |
| EC-03 | heading accentue ou francais | normaliser |
| EC-04 | sections dupliquees | signaler duplicate |
| EC-05 | section vide | detecter mais marquer empty |
| EC-06 | alias non canonique | mapper si connu |
| EC-07 | ordre de sections atypique | accepter |
| EC-08 | markdown malforme | warning |
| EC-09 | frontmatter YAML | ignorer comme contenu section |
| EC-10 | tableau contenant WHY | ne pas detecter comme heading |

## Regles

- Le parser doit privilegier les headings markdown reels.
- Le parser ne doit pas inferer un WHY depuis du texte libre.
- Les sections dupliquees doivent etre conservees avec positions.
- Les sections vides doivent etre visibles dans la sortie.

## Invariant

Un cas limite ne doit jamais conduire a une modification automatique du fichier source.

## RISKS

- À qualifier.
