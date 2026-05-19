# GO_OPENCLAW_ALIGNMENT_DECISION_07

## Classification

- Type : diagnostic ponctuel
- Statut : `READY`
- Portee : decision canonique sur la cible d alignement entre policy V1 et runtime OpenClaw, sans modification runtime dans ce GO

## But

Decider, a partir de l etat reel deja prouve, quelle cible canonique doit etre retenue pour l alignement entre la policy `model_provider_openclaw` et le runtime OpenClaw.

Ce GO ne corrige rien.
Ce GO tranche la cible documentaire et operatoire avant tout patch.

## Repo canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`
- Machine owner : `db-layer`
- Runtime owner : `openclaw`

## Base deja etablie

Le GO precedent a etabli, via lecture du fichier runtime reel `/home/openclaw/.openclaw/openclaw.json`, les constats suivants :

- `orchestrateur` est aligne policy/runtime
- `builder` est aligne policy/runtime
- `reviewer` est explicitement configure en runtime sur `openai/gpt-5.4`, non aligne avec la policy V1 lue
- `lab` est explicitement configure en runtime sur `openrouter/qwen/qwen3-14b`, non aligne avec le primary policy, mais correspondant au fallback policy
- `codexoauth` est explicitement configure au runtime et hors perimetre de la policy V1 lue

## Question de decision

Ce GO doit trancher, pour chaque cas non aligne ou hors perimetre, si la cible canonique doit etre :

- la policy V1 actuelle
- le runtime reel actuel
- une policy V2 explicite
- une exception documentee et assumee

## Matrice de decision attendue

### 1. reviewer

Etat prouve :
- policy V1 : `openrouter / deepseek/deepseek-r1`
- runtime reel : `openai/gpt-5.4`

Decision a prendre :
- **A. realigner le runtime sur la policy V1**
- **B. faire evoluer la policy pour absorber `openai/gpt-5.4` comme cible canonique**
- **C. conserver un ecart documente temporaire**

### 2. lab

Etat prouve :
- policy V1 primary : `openai_compatible_local / qwen3:14b-instruct`
- policy V1 fallback : `openrouter / qwen/qwen3-14b`
- runtime reel : `openrouter / qwen/qwen3-14b`

Decision a prendre :
- **A. revenir au primary policy**
- **B. promouvoir l etat runtime actuel comme cible canonique**
- **C. documenter que le fallback est l etat accepte sur cette machine / ce contexte**

### 3. codexoauth

Etat prouve :
- present au runtime
- absent de la policy V1 lue
- runtime : `openai-codex/gpt-5.4`

Decision a prendre :
- **A. integrer `codexoauth` dans la policy canonique**
- **B. laisser `codexoauth` hors perimetre policy mais comme exception documentee**
- **C. prevoir sa suppression / desactivation dans un GO distinct ulterieur**

## Livrable attendu

Une decision canonique explicite, minimale et non ambiguë sur :

- `reviewer`
- `lab`
- `codexoauth`

avec, pour chacun :
- cible retenue
- justification courte
- consequence sur le chantier suivant

## Conditions de close

Le GO est clos si :

- une cible canonique est decidee pour `reviewer`
- une cible canonique est decidee pour `lab`
- une position canonique est decidee pour `codexoauth`
- il est clair si le prochain chantier est :
  - un patch runtime
  - un patch policy
  - un simple maintien documente de l etat actuel

## Hors perimetre

- toute modification immediate de `~/.openclaw/openclaw.json`
- toute mutation immediate de la policy providers
- toute rotation de credentials ou de token dans ce GO
- toute correction runtime sans decision canonique prealable
- tout commit runtime hors documentation

## Point de reprise suivant

Une fois ce GO clos :

- soit ouvrir un patch local borne de realignement runtime
- soit ouvrir un patch local borne d evolution policy
- soit figer une exception documentaire si l ecart est volontaire et accepte
