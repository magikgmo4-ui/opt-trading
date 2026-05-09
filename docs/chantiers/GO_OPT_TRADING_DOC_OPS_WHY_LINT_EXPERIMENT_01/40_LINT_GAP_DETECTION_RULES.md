# 40_LINT_GAP_DETECTION_RULES

## Objectif

Definir les regles de detection de gaps du WHY lint experimental.

## Gaps candidats

| Gap | Exemple |
| --- | --- |
| WHY absent | justification manquante |
| invariant absent | protection runtime absente |
| recovery path absent | reprise impossible |
| review humaine absente | governance incomplete |
| observabilite absente | preuves runtime absentes |
| runtime class absente | criticite inconnue |

## Regles

- Les gaps critiques doivent etre visibles.
- Les surfaces R4/R5 doivent augmenter la severite.
- Les surfaces multi-machine doivent exposer leurs dependances.
- Les surfaces externes doivent rester contextualisees.

## Observation

Les gaps doivent aider a:
- preparer les reviews humaines,
- renforcer la governance,
- detecter les incoherences runtime.

## Invariant

Le lint WHY ne doit jamais corriger automatiquement un gap documentaire.
