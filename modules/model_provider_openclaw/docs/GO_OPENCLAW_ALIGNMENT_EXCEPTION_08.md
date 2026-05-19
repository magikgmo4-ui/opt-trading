# GO_OPENCLAW_ALIGNMENT_EXCEPTION_08

## Classification

- Type : diagnostic ponctuel
- Statut : `READY`
- Portee : decision canonique de maintien documente des ecarts policy/runtime observes sur `db-layer`, sans modification runtime immediate

## But

Figer une decision canonique minimale a partir de l etat reel deja prouve, sans ouvrir de patch runtime ou policy premature.

Ce GO retient, par defaut, le maintien documente de l etat reel observe pour les cas non alignes ou hors perimetre, tant qu aucun besoin operatoire ne justifie une correction immediate.

## Repo canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`
- Machine owner : `db-layer`
- Runtime owner : `openclaw`

## Base deja etablie

Les lectures precedentes ont etabli :

- `orchestrateur` aligne policy/runtime
- `builder` aligne policy/runtime
- `reviewer` explicitement configure en runtime sur `openai/gpt-5.4`, non aligne avec la policy V1
- `lab` explicitement configure en runtime sur `openrouter/qwen/qwen3-14b`, correspondant au fallback policy
- `codexoauth` explicitement configure au runtime et hors perimetre policy V1

## Decision canonique retenue

### 1. reviewer

Decision retenue : **ecart documente temporaire**

- le runtime actuel `openai/gpt-5.4` est maintenu tel quel sur `db-layer`
- la policy V1 n est pas modifiee dans ce GO
- aucun realignement runtime n est engage immediatement

Justification courte :
- l etat runtime est explicite et prouve
- aucune preuve ne force immediatement un retour vers `deepseek/deepseek-r1`
- une correction sans besoin terrain explicite serait prematuree

### 2. lab

Decision retenue : **fallback accepte sur `db-layer`**

- l etat runtime actuel `openrouter/qwen/qwen3-14b` est maintenu sur cette machine
- la policy V1 primary n est pas promue ni supprimee dans ce GO
- le fallback observe est traite comme etat accepte localement

Justification courte :
- l etat runtime est explicite et prouve
- le runtime correspond deja au fallback policy
- rien n etablit qu un retour immediat au primary soit requis

### 3. codexoauth

Decision retenue : **exception documentee hors policy V1**

- `codexoauth` reste hors perimetre de la policy V1 actuelle
- aucune integration policy ni suppression runtime n est engagee dans ce GO
- son existence au runtime est consideree comme exception explicite et assumee

Justification courte :
- l agent est explicitement present dans la config runtime
- la policy V1 lue ne le couvre pas
- aucune preuve ne permet encore de trancher entre integration canonique ou retrait operatoire

## ETABLI

- la cible canonique immediate n est pas un patch runtime
- la cible canonique immediate n est pas un patch policy
- la position retenue est un maintien documente de l etat actuel pour `reviewer`, `lab` et `codexoauth`

## NON ETABLI

- qu un realignement soit necessaire a court terme
- que la policy V1 doive absorber immediatement l etat runtime reel
- que `codexoauth` doive devenir un agent policy canonique dans l immediate

## RUNBOOK

Ce document n est pas un runbook de correction.

Lecture operative :
- conserver l etat runtime tel quel sur `db-layer`
- ne pas muter la policy V1 dans ce GO
- ne pas ouvrir de patch runtime sans besoin operatoire explicite
- reouvrir un GO distinct seulement si un usage terrain, un incident ou une contrainte d harmonisation impose une action

## RISQUES / POINTS DE VIGILANCE

- confondre maintien documente et validation definitive globale
- etendre a d autres machines une decision prise a partir de `db-layer` seul
- engager un patch runtime ou policy sans nouveau fait operatoire
- recopier en documentation des secrets issus du fichier `openclaw.json`

## CHANGELOG

- `ALIGNMENT_EXCEPTION_08` : decision canonique de maintien documente des ecarts observes sur `reviewer`, `lab` et `codexoauth`
- aucun changement runtime
- aucune mutation de policy
- aucune exposition de secret en documentation

## Conditions de close

Le GO est clos si :

- une decision explicite existe pour `reviewer`
- une decision explicite existe pour `lab`
- une decision explicite existe pour `codexoauth`
- il est clair qu aucun patch runtime ni policy n est ouvert immediatement
- le prochain chantier depend d un besoin operatoire reel et non d une hypothese

## Hors perimetre

- toute modification immediate de `~/.openclaw/openclaw.json`
- toute mutation immediate de la policy providers
- toute rotation de credentials ou de token dans ce GO
- toute correction runtime sans fait operatoire nouveau
- tout commit runtime hors documentation

## Point de reprise suivant

Une fois ce GO fige :

- soit ne rien ouvrir tant qu aucun besoin operatoire nouveau n apparait
- soit ouvrir un patch local borne si un realignement runtime devient necessaire
- soit ouvrir un patch policy borne si la policy doit absorber durablement un etat runtime prouve
