# GO OPENCLAW SYNC 02

## Classification

- Type : synchronisation documentaire canonique
- Statut : `READY`
- Portee : preuves runtime deja etablies sur `db-layer`, sans modification runtime

## But

Consigner de maniere canonique l etat de synchronisation OpenClaw deja prouve sur `db-layer`, a partir des seuls faits etablis, sans invention ni extrapolation.

## Repo canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## Source de verite retenue

La source de verite retenue pour ce document est l ensemble des preuves runtime deja etablies sur `db-layer`, bornees aux faits suivants :

- `user = openclaw`
- `host = db-layer`
- `workspace = /home/openclaw/.openclaw/workspace-orchestrateur`
- configuration valide `~/.openclaw/openclaw.json`
- 5 agents presents : `orchestrateur`, `builder`, `reviewer`, `lab`, `codexoauth`
- gateway loopback `ws://127.0.0.1:18789` : `OK`
- gateway `db-layer = 192.168.0.100`
- version app : `2026.4.2`
- double state dir a surveiller avec `/home/ghost/.openclaw` en vigilance

## ETABLI

Les faits suivants sont etablis et seulement ceux-ci :

- l utilisateur de reference est `openclaw`
- l hote de reference est `db-layer`
- le workspace de reference est `/home/openclaw/.openclaw/workspace-orchestrateur`
- le fichier de configuration `~/.openclaw/openclaw.json` est valide
- 5 agents sont etablis dans le perimetre observe :
  - `orchestrateur`
  - `builder`
  - `reviewer`
  - `lab`
  - `codexoauth`
- la gateway loopback `ws://127.0.0.1:18789` est `OK`
- la gateway associee a `db-layer` est `192.168.0.100`
- la version applicative relevee est `2026.4.2`
- une vigilance existe sur un double state dir impliquant `/home/ghost/.openclaw`

## RUNBOOK

Ce document n est pas un runbook d execution.

Lecture minimale des preuves retenues :

- identite d execution : `openclaw@db-layer`
- workspace de reference : `/home/openclaw/.openclaw/workspace-orchestrateur`
- configuration valide : `~/.openclaw/openclaw.json`
- perimetre agents observe : 5 agents
- connectivite gateway locale prouvee en loopback : `ws://127.0.0.1:18789`
- adresse relevee pour `db-layer` : `192.168.0.100`
- version app relevee : `2026.4.2`
- point de vigilance : coexistence d un second state dir sous `/home/ghost/.openclaw`

## CHANGELOG

- `SYNC-02` : consolidation documentaire canonique des preuves runtime deja etablies sur `db-layer`
- aucun fait nouveau ajoute
- aucune modification runtime
- aucune reinterpretation au-dela des preuves retenues

## Conditions de close

Le document est clos si et seulement si :

- les preuves etablies sont reprises sans invention
- l identite `openclaw@db-layer` est explicite
- le workspace canonique est explicite
- la validite de `~/.openclaw/openclaw.json` est explicite
- les 5 agents sont listes explicitement
- la gateway loopback `ws://127.0.0.1:18789` est notee `OK`
- l adresse `192.168.0.100` est consignee comme gateway `db-layer`
- la version `2026.4.2` est consignee
- la vigilance sur le double state dir avec `/home/ghost/.openclaw` est explicite
- aucune extrapolation ni modification runtime n apparait

## Hors perimetre

- toute installation
- toute modification runtime
- toute correction de configuration
- toute fusion ou suppression de state dir
- toute interpretation sur les causes du double state dir
- toute ouverture reseau supplementaire
- tout ajout d agent non prouve
- tout changement de version applicative
- tout commit git

## Point de reprise suivant

Plus petit prochain pas utile :

- verifier documentairement si la vigilance sur le double state dir doit faire l objet d un document canonique distinct, sans modifier le runtime existant.
