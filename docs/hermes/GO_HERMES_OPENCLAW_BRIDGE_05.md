# GO_HERMES_OPENCLAW_BRIDGE_05

## Classification
Type : patch local borne

## But

Ouvrir le prochain GO logique de la séquence OpenClaw : une première preuve courte Hermes -> OpenClaw -> validation humaine.

Ce GO ne prétend pas qu un bridge complet est déjà établi. Il borne seulement le cas de preuve à viser et les règles à respecter.

## Base documentaire déjà établie

Le repo contient déjà `docs/hermes/03_bridge_openclaw.md`, qui fixe :
- un objectif de flux simple ;
- une structure visée `tools/hermes_bridge/` ;
- un workflow minimal ;
- les garde-fous : pas d auto-commit, pas d exécution non contrôlée, validation obligatoire.

## Lecture canonique pour ce GO

1. `docs/hermes/03_bridge_openclaw.md`
2. `docs/hermes/HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md`
3. les documents OpenClaw récemment clos dans la chaîne `GO_OPENCLAW_*`

## Cas de preuve à viser

Le premier cas doit rester :
- petit ;
- lisible ;
- réversible ;
- sans exposition réseau nouvelle ;
- sans mutation système large.

Exemple de forme attendue :
- Hermes génère un artefact borné
- OpenClaw relit ou exécute dans un cadre contrôlé
- le résultat est observé
- la validation humaine tranche explicitement

## Garde-fous

- pas d auto-commit
- pas d exécution non contrôlée
- validation humaine obligatoire avant intégration
- ne pas transformer ce GO en chantier produit large
- ne pas lire une preuve unique comme maturité générale du bridge

## Livrables minimaux

- un cas de preuve borné choisi explicitement
- l artefact généré par Hermes
- la preuve côté OpenClaw
- la validation humaine
- une note de résultat courte

## Condition de close

Le GO est clos si :
- un premier cas de preuve a été exécuté de bout en bout ;
- la validation humaine est explicitement tracée ;
- les garde-fous ont été respectés ;
- le résultat est documenté sans extrapolation.

## Hors périmètre

- pas de bridge général déclaré établi
- pas de framework complet `tools/hermes_bridge/` déclaré comme livré si la preuve ne porte que sur un cas unique
- pas de production large
- pas de déplacement de runtime dans le repo `openclaw`

## Point de reprise suivant

Après ce GO :
- soit formaliser un second cas de preuve si le premier reste trop étroit ;
- soit ouvrir un micro-module bridge si plusieurs preuves bornées convergent ;
- sinon clore le sujet comme preuve ponctuelle suffisante.
