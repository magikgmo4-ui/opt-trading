# GO_OPENCLAW_STATE_DIR_REPAIR_10

## Classification

- Type : diagnostic ponctuel
- Statut : READY
- Portee : reparation locale bornee du gateway OpenClaw sur `db-layer`

## Repo canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`
- Hote vise : `db-layer`
- Runtime owner attendu : `openclaw`
- GO amont : `GO_OPENCLAW_STATE_DIR_READ_09`
- Verdict amont : `REPAIR LOCAL`

## Etat de depart retenu

Etat retenu exclusivement depuis la lecture machine-sourcee `READ_09` :

- la config lue et validee est `~/.openclaw/openclaw.json`
- le workspace detecte est `/home/openclaw/.openclaw/workspace-orchestrateur`
- la session `openclaw-gateway` est arretee
- la cible gateway attendue reste `ws://127.0.0.1:18789`
- la gateway locale n est pas joignable
- le refus observe est `ECONNREFUSED 127.0.0.1:18789`

Point de vigilance retenu sans causalite affirmee :

- un double state dir reste documente comme vigilance
- ce GO ne pose pas que ce double state dir soit la cause de l indisponibilite gateway

## Objectif

Retablir localement, sur `db-layer`, le fonctionnement du gateway OpenClaw attendu en loopback pour l utilisateur `openclaw`.

Le but borne de ce GO est :

- remettre la session `openclaw-gateway` dans un etat operatoire local
- retablir la joignabilite de `ws://127.0.0.1:18789`
- verifier la disparition du `ECONNREFUSED 127.0.0.1:18789`

## Perimetre

- verification locale des prerequis immediats du gateway
- relance locale du gateway via le module `gateway_openclaw`
- verification locale `status`, `health`, `probe`, `logs`
- qualification factuelle du retour a l etat operatoire ou de l echec local

## Hors perimetre

- tout `PATCH RUNTIME` large
- tout `PATCH POLICY`
- toute mutation de policy provider/model
- toute conclusion causale sur le double state dir sans preuve nouvelle
- toute exposition WAN ou hors loopback
- toute rearchitecture multi-machine
- toute correction non necessaire au retablissement local du gateway

## Sequence de diagnostic-reparation minimale

Execution attendue sous `openclaw` sur `db-layer`.

### 1. Relecture locale avant action

```bash
cd /opt/trading
bash modules/gateway_openclaw/scripts/cmd.sh status
bash modules/gateway_openclaw/scripts/cmd.sh paths
bash modules/doctor_openclaw/scripts/cmd.sh status
```

### 2. Reparation locale bornee

```bash
cd /opt/trading
bash modules/gateway_openclaw/scripts/cmd.sh start
```

### 3. Verification immediate

```bash
cd /opt/trading
bash modules/gateway_openclaw/scripts/cmd.sh status
bash modules/gateway_openclaw/scripts/cmd.sh health
bash modules/gateway_openclaw/scripts/cmd.sh probe
bash modules/gateway_openclaw/scripts/cmd.sh logs
```

### 4. Qualification de sortie

Sortie attendue :

- soit gateway locale retablie en loopback
- soit echec local qualifie avec preuve exploitable pour la suite

## Criteres de close

Le GO est clos si :

- la session `openclaw-gateway` n est plus arretee
- `ws://127.0.0.1:18789` repond localement ou l echec restant est qualifie factuellement
- le `ECONNREFUSED 127.0.0.1:18789` a disparu ou son maintien est explique par une preuve locale nouvelle
- aucune extension de scope vers runtime large ou policy n a ete ouverte

## Point de reprise

- si la reparation locale suffit : retour a une passe de verification runtime et preuves locales
- si la reparation locale echoue avec fait technique nouveau borne : ouvrir `GO_OPENCLAW_ALIGNMENT_RUNTIME_PATCH_11`
- si aucun fait runtime nouveau ne depasse le scope local : ne pas ouvrir de `PATCH POLICY`
