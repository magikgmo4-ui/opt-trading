# Architecture Hermes Lab

## Pattern

Hermes -> generation
OpenClaw -> execution
opt-trading -> validation canonique

## Flux operatoire

1. Hermes genere un artefact
2. Execution controlee
3. Observation resultat
4. Validation humaine
5. Integration repo

## Separation

Hermes = memoire de travail
Repo = memoire officielle

## Regle critique

Hermes ne modifie jamais directement le repo
