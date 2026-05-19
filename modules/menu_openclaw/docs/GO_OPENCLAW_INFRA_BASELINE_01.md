# GO_OPENCLAW_INFRA_BASELINE_01

## Classification

Type : diagnostic ponctuel
Statut : READY

## But

Fixer le baseline infra retenu pour l usage OpenClaw dans `opt-trading`, sans le confondre avec une preuve machine déjà revalidée.

Ce GO :

- fixe la décision infra
- fixe le cloisonnement cible
- rappelle que `db-layer` est le point d entrée canonique
- interdit l exposition publique par défaut
- impose que la suite parte d un read-only machine-sourcé

Ce GO n est pas :

- un GO de preuve machine
- un GO de réparation
- un GO de patch runtime
- un GO de patch policy

## Repo canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## Portée

Décision infra documentaire uniquement.

Aucune mutation runtime.
Aucune correction de config.
Aucune ouverture WAN.
Aucun mélange prématuré avec OPS trading.

## ETABLI

À ce stade, les points suivants peuvent être tenus comme établis dans le canon documentaire courant :

- OpenClaw est cadré dans `opt-trading` comme cockpit opérateur local sur `db-layer`
- le runtime documentaire de référence est `openclaw@db-layer`
- le workspace documentaire de référence est `/home/openclaw/.openclaw/workspace-orchestrateur`
- la config documentaire de référence est `~/.openclaw/openclaw.json`
- la gateway loopback `ws://127.0.0.1:18789` a déjà une preuve documentaire
- un second state dir `/home/ghost/.openclaw` est documenté comme point de vigilance
- le canon actuel ne justifie pas de patch immédiat sur `reviewer`, `lab` ou `codexoauth`

## BASELINE INFRA RETENUE

Le baseline infra retenu pour la suite du chantier est le suivant :

### Hôte canonique

- `db-layer` = hôte canonique OpenClaw

### Surfaces séparées

- `Windows` = surface opérateur visée pour UI / capture / pilotage
- `admin-trading` = OPS trading séparé du runtime OpenClaw principal
- `fantome` = candidat futur seulement si un besoin réel d isolement supplémentaire apparaît

### Baseline technique visée

- OpenClaw reste d abord local sur `db-layer`
- gateway / dashboard / websocket restent en loopback
- port attendu : `18789`
- bind attendu : `127.0.0.1`
- exécution prudente en user-space
- sandbox active
- `browser.enabled = false`
- `tools.elevated.enabled = false`
- `tools.loopDetection.enabled = true`
- aucune exposition WAN par défaut

### Règles de séparation

- ne pas héberger le runtime OpenClaw principal sur `Windows`
- ne pas mélanger trop tôt OpenClaw et runtime trading sur `admin-trading`
- ne pas exposer publiquement la gateway tant que le baseline n est pas qualifié
- toute correction doit partir de l état réel observé sur `db-layer`

## A CONFIRMER DANS LE GO SUIVANT

Les points suivants ne sont pas re-prouvés par ce GO et doivent rester à confirmer dans la prochaine passe machine :

- state dir réellement actif maintenant
- config réellement active maintenant
- logs réellement actifs maintenant
- état réel gateway / dashboard / doctor maintenant
- impact réel ou non du double state dir
- conformité machine réelle à la baseline visée

## ORDRE DE CHANTIER RETENU

L ordre de chantier validé est :

1. vérifier l état réel OpenClaw sur `db-layer`
2. fermer le diagnostic state dir / config / logs / doctor
3. statuer sur la stabilité du runtime local canonique
4. produire les preuves runtime mises à jour
5. seulement ensuite décider les accès opérateur depuis `Windows`
6. reporter toute extension vers `admin-trading` ou `fantome` en phase 2

## GO IMMÉDIAT DE REPRISE

Le GO immédiat de reprise est :

- `GO_OPENCLAW_STATE_DIR_READ_09`

## PÉRIMÈTRE DE LECTURE DU GO IMMÉDIAT

Le `READ_09` doit rester strictement lecture-only et couvrir :

- identification du state dir réellement utilisé
- vérification de la config active
- vérification des logs actifs
- vérification de `doctor`, `gateway` et `dashboard`
- confirmation du caractère réel, neutre ou bloquant du double state dir

## GO INTERDITS AVANT VERDICT DU READ_09

Aucun patch ni réparation avant fermeture du `READ_09`.

Les GO suivants sont explicitement interdits avant verdict machine-sourcé :

- `GO_OPENCLAW_STATE_DIR_REPAIR_10`
- `GO_OPENCLAW_ALIGNMENT_RUNTIME_PATCH_11`
- `GO_OPENCLAW_POLICY_V2_12`

## SORTIES AUTORISÉES DU READ_09

La sortie décisionnelle du `READ_09` doit être strictement l une des suivantes :

- `NO-OP`
- `REPAIR LOCAL`
- `PATCH RUNTIME`
- `PATCH POLICY`

## NON ETABLI

Ce GO n établit pas :

- que la baseline technique visée soit déjà conforme en machine dans cette passe
- que le double state dir ait déjà un impact qualifié
- qu une réparation soit déjà nécessaire
- qu un patch runtime soit déjà justifié
- qu une policy V2 soit déjà requise

## HORS PÉRIMÈTRE

- toute réparation du state dir
- toute mutation de `~/.openclaw/openclaw.json`
- toute modification de la gateway en exposition réseau
- toute extension OpenClaw vers `admin-trading`
- toute bascule du runtime principal vers `Windows`
- toute généralisation infra non prouvée
- tout patch policy avant lecture machine réelle

## CONDITION DE CLOSE

Ce GO est clos si :

- la séparation entre décision infra et preuve machine est explicite
- `db-layer` est fixé comme point d entrée canonique
- le baseline infra retenu est écrit sans sur-vendre son statut de preuve
- le `GO_OPENCLAW_STATE_DIR_READ_09` est ouvert explicitement comme premier GO opératoire réel
- aucun patch n est ouvert avant verdict machine-sourcé

## POINT DE REPRISE SUIVANT

- `GO_OPENCLAW_STATE_DIR_READ_09`

Ensuite seulement, selon verdict :

- `GO_OPENCLAW_STATE_DIR_REPAIR_10`
- `GO_OPENCLAW_ALIGNMENT_RUNTIME_PATCH_11`
- `GO_OPENCLAW_POLICY_V2_12`
