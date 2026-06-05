# 130_WHY_PARSER_ARCHITECTURE_SYNTHESIS

## Objectif

Synthétiser l'architecture du futur parser markdown WHY.

## Synthese

Le chantier definit un parser documentaire WHY:
- lecture seule,
- non destructif,
- audit-oriented,
- explicable,
- compatible multi-machine,
- prepare pour scoring futur.

## Architecture retenue

| Couche | Role |
| --- | --- |
| sections spec | definir les headings WHY detectables |
| output schema | normaliser la sortie |
| gap rules | detecter les manques critiques |
| scoring preparation | preparer score futur |
| edge cases | traiter markdown ambigu |
| false positive policy | reduire detections abusives |
| runtime limits | bloquer toute autorite runtime |
| state machine | definir pipeline parser |
| document priority | prioriser les surfaces critiques |
| multi-machine context | integrer contexte machine |
| worker roadmap | preparer audit futur |

## Etat parser cible

Le parser doit passer par:
1. DISCOVER
2. LOAD
3. NORMALIZE
4. SEGMENT
5. CLASSIFY
6. VALIDATE
7. SCORE_PREP
8. REPORT

Avec sorties explicites:
- SKIP,
- ERROR.

## Pourquoi cette architecture existe

Le WHY layer doit pouvoir etre lu automatiquement sans creer:
- faux positif critique,
- enforcement premature,
- APPLY automatique,
- validation runtime autonome.

## Resultat attendu

Les futurs chantiers peuvent utiliser ce cadrage pour implementer:
- parser markdown,
- score generator,
- worker audit,
- lint experimental,
- dashboard governance.

## Invariant final

Le parser WHY ne doit jamais modifier les documents sources ni remplacer une review humaine sur surface critique.

## RISKS

- À qualifier.
