# GO_OPENCLAW_STATE_DIR_VIGILANCE_03

## Classification

- Type : diagnostic ponctuel
- Statut : `READY`
- Portee : vigilance documentaire sur double state dir OpenClaw, sans modification runtime

## But

Consigner de maniere canonique la vigilance sur le double state dir observe dans les preuves runtime OpenClaw, sans deduire de cause et sans intervenir sur le runtime existant.

## Repo canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## Source de verite retenue

Ce document part uniquement des preuves runtime deja etablies sur `db-layer`, en particulier du constat suivant :

- le state dir actif indique est `~/.openclaw`
- un state dir supplementaire est detecte : `/home/ghost/.openclaw`
- le doctor indique que cette situation peut fragmenter l historique de session

## ETABLI

- l execution de reference est `openclaw@db-layer`
- le state dir actif indique dans les preuves est `~/.openclaw`
- un second state dir a ete detecte sous `/home/ghost/.openclaw`
- le doctor signale que des state directories multiples peuvent scinder l historique de session
- aucune correction runtime n a ete appliquee dans ce GO

## NON ETABLI

- la cause exacte de la presence de `/home/ghost/.openclaw`
- le niveau d impact reel sur les sessions en cours
- la necessite immediate d une correction runtime
- la strategie correcte de fusion, suppression ou migration

## RISQUES / POINTS DE VIGILANCE

- confusion entre etat actif et etat historique
- lecture erronee de l historique de session
- action de nettoyage prematuree sans preuve complementaire
- perte de continuite si une correction est appliquee sans cadrage

## RUNBOOK

Ce document n est pas un runbook de correction.

Lecture minimale :
- retenir que `~/.openclaw` est l etat actif signale
- retenir que `/home/ghost/.openclaw` est un point de vigilance
- ne pas corriger ni supprimer sans GO distinct et preuves complementaires

## CHANGELOG

- `STATE_DIR_VIGILANCE_03` : isolement documentaire du risque lie au double state dir
- aucun changement runtime
- aucune reinterpretation causale
- aucune action corrective engagee

## Conditions de close

Le document est clos si et seulement si :
- le double state dir est consigne sans invention
- l etat actif et l etat supplementaire sont distingues explicitement
- aucun plan de correction n est affirme sans preuves complementaires
- le risque documentaire est borne clairement

## Hors perimetre

- suppression de `/home/ghost/.openclaw`
- fusion de state dirs
- correction automatique via doctor
- modification de config
- changement d agent
- changement de gateway
- tout commit runtime hors documentation

## Point de reprise suivant

Plus petit prochain pas utile :
- ouvrir un GO distinct seulement si une verification technique complementaire du double state dir devient necessaire, avec commandes de lecture uniquement en premiere passe.
