# Frontiere OpenClaw lab differee

## Etat retenu

- `OpenClaw` est absent sur `student`
- `OpenClaw lab` reste donc `NON_QUALIFIE`

## Ce que le child a etabli

- aucune commande `openclaw` n'est presente sur `student`
- aucune version `openclaw` n'est remontee
- aucune installation n'a ete faite
- aucune activation lab n'a ete tentee

## Decision parent

- `student` est valide comme machine `Ollama`
- `student` n'est pas encore valide comme machine `OpenClaw lab`
- le parent conserve `OpenClaw` comme piste d'orchestration future, mais explicitement differee

## Invariants

- installation interdite dans ce GO
- `db-layer` garde le runtime principal `OpenClaw`
- aucun deplacement de runtime hors `db-layer`
- aucun changement `admin-trading`

## Conditions d'un futur GO si necessaire

- validation explicite d'une installation ou mise a disposition `OpenClaw`
- confirmation de compatibilite provider `OpenClaw <-> Ollama`
- garde-fous lab : localhost, pas de secrets, pas de shell libre, pas d'ecriture repo automatique
- reouverture du child seulement si ces conditions sont levees
