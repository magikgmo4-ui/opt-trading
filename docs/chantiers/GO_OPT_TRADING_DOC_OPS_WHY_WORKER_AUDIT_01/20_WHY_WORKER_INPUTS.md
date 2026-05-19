# 20_WHY_WORKER_INPUTS

## Objectif

Definir les entrees du futur worker WHY.

## Entrees candidates

| Entree | Source |
| --- | --- |
| sections detectees | parser WHY |
| gaps documentaires | parser WHY |
| score WHY | score generator |
| runtime class R0-R5 | runtime governance |
| observabilite | runtime docs |
| review humaine | reviews runtime |
| reprise | RESUME_POINT |

## Types de donnees

| Type | Role |
| --- | --- |
| markdown | documents sources |
| json | sorties parser/scoring |
| reports | syntheses audit |

## Observation

Le worker doit privilegier:
- les donnees explicites,
- les preuves documentaires,
- les sections structurees.

## Invariant

Le worker WHY ne doit jamais inventer des donnees runtime absentes.
