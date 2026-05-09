# 70_WHY_WORKER_HUMAN_REVIEW_POLICY

## Objectif

Proteger la review humaine dans le futur systeme WHY.

## Principes

Le worker WHY:
- assiste,
- signale,
- explique,
- prepare des reviews.

Il ne valide jamais seul un runtime critique.

## Surfaces critiques

| Classe | Politique |
| --- | --- |
| R0 | review optionnelle |
| R1 | review recommandee |
| R2 | review contextualisee |
| R3 | review forte |
| R4 | review humaine obligatoire |
| R5 | governance humaine maximale |

## Cas bloquants humains

| Cas | Action |
| --- | --- |
| runtime non prouve | review humaine |
| observabilite absente | review humaine |
| incoherence governance | review humaine |
| gaps critiques | review humaine |

## Invariant

Le worker WHY ne doit jamais remplacer une decision humaine sur surface critique.
