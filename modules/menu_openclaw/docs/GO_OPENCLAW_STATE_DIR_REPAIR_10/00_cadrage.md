# GO_OPENCLAW_STATE_DIR_REPAIR_10

## Classification

- Type : diagnostic ponctuel
- Statut : READY
- Portee : reparation locale bornee du gateway OpenClaw sur `db-layer`, dans le contexte utilisateur `openclaw`

## Repo canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`
- Hote vise : `db-layer`
- Runtime owner attendu : `openclaw`
- GO amont : `GO_OPENCLAW_STATE_DIR_READ_09`
- Verdict amont : `REPAIR LOCAL`

## Etat de depart retenu

Etat retenu depuis la lecture machine-sourcee et la revue runtime `db-layer` :

- la config lue et validee est `~/.openclaw/openclaw.json`
- le workspace detecte est `/home/openclaw/.openclaw/workspace-orchestrateur`
- la session `openclaw-gateway` est arretee
- la cible gateway attendue reste `ws://127.0.0.1:18789`
- la gateway locale n est pas joignable
- le refus observe est `ECONNREFUSED 127.0.0.1:18789`

Diagnostic prioritaire retenu :

- le runtime owner attendu est `openclaw`
- les controles et actions doivent etre executes sous `openclaw`, pas dans le contexte de l utilisateur SSH courant
- le probleme principal a traiter est l absence du gateway dans la session utilisateur `openclaw`

Verification owner/runtime attendue avant action :

- existence de l utilisateur `openclaw`
- `HOME` reel, shell et `PATH`
- disponibilite du binaire `openclaw`
- version `openclaw` dans ce contexte utilisateur
- presence des fichiers et logs runtime sous le `HOME` de `openclaw`

Point de vigilance secondaire seulement :

- un double state dir reste documente comme vigilance
- ce GO ne pose pas que ce double state dir soit la cause de l indisponibilite gateway
- le state dir ne devient un axe de verification qu en cas d echec du demarrage controle du gateway

## Objectif

Retablir localement, sur `db-layer`, le fonctionnement du gateway OpenClaw attendu en loopback pour l utilisateur `openclaw`.

Le but borne de ce GO est :

- verifier explicitement le contexte runtime `openclaw`
- remettre la session `openclaw-gateway` dans un etat operatoire local
- retablir la joignabilite de `ws://127.0.0.1:18789`
- verifier la disparition du `ECONNREFUSED 127.0.0.1:18789`

## Perimetre

- verification locale du runtime owner `openclaw`
- verification locale des prerequis immediats du gateway
- lecture de l aide CLI et de la documentation locale pour confirmer la commande exacte
- relance locale du gateway via le module `gateway_openclaw` ou la commande exacte confirmee
- verification locale `status`, `health`, `probe`, `logs`
- qualification factuelle du retour a l etat operatoire ou de l echec local

## Hors perimetre

- tout `PATCH RUNTIME` large
- tout `PATCH POLICY`
- toute mutation de policy provider/model
- toute conclusion causale sur le double state dir sans preuve nouvelle
- toute exposition WAN ou hors loopback
- toute rearchitecture multi-machine
- toute suppression ou modification de state dir sans preuve et sans backup dedie
- toute correction non necessaire au retablissement local du gateway

## Sequence de diagnostic-reparation minimale

Execution attendue sous `openclaw` sur `db-layer`.

### 1. Relecture locale avant action

```bash
getent passwd openclaw
sudo -iu openclaw bash -lc 'whoami; hostname; pwd; echo HOME=$HOME; echo PATH=$PATH'
sudo -iu openclaw bash -lc 'command -v openclaw; openclaw --version'
cd /opt/trading
bash modules/gateway_openclaw/scripts/cmd.sh status
bash modules/gateway_openclaw/scripts/cmd.sh paths
bash modules/doctor_openclaw/scripts/cmd.sh status
```

### 2. Confirmation de la commande runtime

```bash
sudo -iu openclaw bash -lc 'openclaw --help | head -120'
sudo -iu openclaw bash -lc 'openclaw gateway --help | head -120'
```

La commande de demarrage ne doit etre lancee qu apres confirmation par :

- l aide CLI
- la documentation locale
- ou le script repo-side `modules/gateway_openclaw/scripts/start.sh`

### 3. Reparation locale bornee

```bash
sudo -iu openclaw
cd /opt/trading
bash modules/gateway_openclaw/scripts/cmd.sh start
```

### 4. Verification immediate

```bash
sudo -iu openclaw
cd /opt/trading
bash modules/gateway_openclaw/scripts/cmd.sh status
bash modules/gateway_openclaw/scripts/cmd.sh health
bash modules/gateway_openclaw/scripts/cmd.sh probe
bash modules/gateway_openclaw/scripts/cmd.sh logs
tmux ls
ss -ltnp | grep 18789
curl -fsS http://127.0.0.1:18789/ | head -40
```

### 5. Escalade secondaire seulement si echec

- verifier la piste `state_dir` seulement si le gateway refuse de demarrer
- ne rien supprimer
- ne rien reparer sans preuve
- backup obligatoire avant toute modification de config ou de state dir

### 6. Qualification de sortie

Sortie attendue :

- soit gateway locale retablie en loopback
- soit echec local qualifie avec preuve exploitable pour la suite

## Criteres de close

Le GO est clos si :

- l utilisateur `openclaw` est verifie
- la session `openclaw-gateway` n est plus arretee
- `ws://127.0.0.1:18789` repond localement ou l echec restant est qualifie factuellement
- le `ECONNREFUSED 127.0.0.1:18789` a disparu ou son maintien est explique par une preuve locale nouvelle
- un process equivalent `openclaw` / `openclaw-gateway` est present ou une session `tmux` equivalente est etablie
- aucune extension de scope vers runtime large ou policy n a ete ouverte

## Point de reprise

- si la reparation locale suffit : retour a une passe de verification runtime et preuves locales
- si la reparation locale echoue avec fait technique nouveau borne : ouvrir `GO_OPENCLAW_ALIGNMENT_RUNTIME_PATCH_11`
- si aucun fait runtime nouveau ne depasse le scope local : ne pas ouvrir de `PATCH POLICY`
