# GO_OPENCLAW_ALIGNMENT_READ_06

## Classification

- Type : diagnostic ponctuel
- Statut : `READY`
- Portee : verification lecture-only de l intention runtime pour `reviewer`, `lab` et `codexoauth`

## But

Determiner a partir du runtime reel, sans aucune modification, si les ecarts observes entre la policy V1 et le runtime OpenClaw relevent :

- d un drift accepte
- d une transition en cours
- d un besoin reel d alignement operatoire

Ce GO ne corrige rien.
Ce GO lit et borne.

## Repo canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`
- Machine owner : `db-layer`
- Runtime owner : `openclaw`

## Base deja etablie

Le GO precedent a deja etabli :

- `orchestrateur` aligne policy/runtime
- `builder` aligne policy/runtime
- `reviewer` non aligne dans l etat observe
- `lab` non aligne avec le primary observe, mais correspondant au fallback policy
- `codexoauth` visible au runtime mais hors perimetre policy V1 lue

## Question precise de ce GO

Lire le runtime reel pour determiner si l etat observe sur `reviewer`, `lab` et `codexoauth` est :

- explicitement configure et donc probablement intentionnel
- herite / transitoire / incomplet
- ou insuffisamment borne pour conclure

## Preconditions

- execution sous l utilisateur `openclaw`
- lecture uniquement
- aucune commande `set`, `unset`, `wizard`, `repair-safe`, `doctor --fix` ou equivalent

## Sequence operatoire minimale

### 1. Identifier le fichier de config reel

```bash
sudo -iu openclaw
cd /opt/trading
CFG="$(bash modules/configure_openclaw/scripts/cmd.sh config-file)"
echo "$CFG"
```

### 2. Relire la config et l inventaire agents

```bash
bash modules/configure_openclaw/scripts/cmd.sh validate
bash modules/configure_openclaw/scripts/cmd.sh agents-list
sed -n '1,240p' "$CFG"
```

### 3. Isoler les indices utiles dans la config

```bash
grep -nE 'reviewer|lab|codexoauth|provider|model|fallback|openrouter|openai_compatible_local|deepseek|gpt-5.4|qwen3' "$CFG" || true
```

### 4. Refiger la policy lue pour comparaison

```bash
bash modules/model_provider_openclaw/scripts/cmd.sh export-json
```

## Sortie attendue

Une sortie lisible qui permet de statuer, pour `reviewer`, `lab` et `codexoauth`, entre :

- ETAT EXPLICITE DANS LA CONFIG
- ETAT OBSERVE SANS INTENTION EXPLICITE PROUVEE
- HORS PERIMETRE POLICY V1
- INSUFFISANT POUR CONCLURE

## Conditions de close

Le GO est clos si :

- le fichier de config reel est identifie
- son contenu utile est relu en lecture seule
- les indices concernant `reviewer`, `lab` et `codexoauth` sont extraits
- une conclusion strictement probante est possible sans modifier le runtime

## Hors perimetre

- toute correction de config
- toute mutation de modele runtime
- toute integration automatique de la policy dans le runtime
- toute suppression ou ajout d agent
- toute ouverture reseau supplementaire
- tout commit runtime hors documentation

## Point de reprise suivant

Une fois ce GO clos :

- soit ouvrir un GO de decision documentaire si l intention est prouvee
- soit ouvrir un patch local borne si un alignement operatoire est reellement requis
- soit conserver l etat comme drift accepte si c est explicitement etabli
