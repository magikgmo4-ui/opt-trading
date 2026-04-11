# GO_OPENCLAW_USAGE_EXAMPLES_09

## Classification
Type : patch local borne
Statut : READY

## But

Fixer le projet cible réel OpenClaw dans `opt-trading` et lister les usages utiles effectivement portés par les modules existants. Établir les frontières explicites de non-périmètre et le point de reprise logique suivant.

Ce document ne spécule pas. Il ne fait que reprendre les faits prouvables par la documentation et les scripts lus.

## Projet cible réel

- Cockpit opérateur local sur `db-layer`
- User/runtime owner de référence : `openclaw`
- Workspace de référence : `~/.openclaw/workspace-orchestrateur`
- Gateway loopback local via `tmux`
- Chaîne orientée : install → config → gateway → configure → doctor → evidence → policy

## Modules déclarés dans la registry

```json
[
  "install_module_openclaw",
  "openclaw_config_modulaire",
  "model_provider_openclaw",
  "configure_openclaw",
  "doctor_openclaw",
  "evidence_openclaw",
  "gateway_openclaw"
]
```

 Registry : `modules/install_module_openclaw/app/modules_registry.json`

## Exemples d usages utiles prouvés

### Hub de reprise via menu_openclaw

```bash
bash modules/menu_openclaw/scripts/cmd.sh status
bash modules/menu_openclaw/scripts/cmd.sh list-menus
bash modules/menu_openclaw/scripts/cmd.sh open-menu gateway_openclaw
```

Commandes : `sanity`, `status`, `list-menus`, `open-menu`, `useful`

### Lecture policy provider/model

```bash
bash modules/model_provider_openclaw/scripts/cmd.sh status
bash modules/model_provider_openclaw/scripts/cmd.sh show-agent orchestrateur
bash modules/model_provider_openclaw/scripts/cmd.sh export-json
```

Providers autorisés : `openrouter`, `openai_compatible_local`
Providers refusés : tout provider non listé explicitement

### Lecture et validation de config

```bash
bash modules/configure_openclaw/scripts/cmd.sh status
bash modules/configure_openclaw/scripts/cmd.sh validate
bash modules/configure_openclaw/scripts/cmd.sh config-file
```

Commandes : `sanity`, `status`, `validate`, `config-file`, `wizard`, `dashboard`, `agents-list`

### Diagnostic runtime

```bash
bash modules/doctor_openclaw/scripts/cmd.sh quick
bash modules/doctor_openclaw/scripts/cmd.sh status
bash modules/doctor_openclaw/scripts/cmd.sh logs
```

Commandes : `sanity`, `quick`, `deep`, `repair-safe`, `validate`, `health`, `probe`, `logs`, `status`

### Pilotage gateway local via tmux

```bash
bash modules/gateway_openclaw/scripts/cmd.sh status
bash modules/gateway_openclaw/scripts/cmd.sh start
bash modules/gateway_openclaw/scripts/cmd.sh attach
bash modules/gateway_openclaw/scripts/cmd.sh logs
```

Session tmux par défaut : `openclaw-gateway`
Log par défaut : `~openclaw/.openclaw/logs/gateway_foreground.log`
Commandes : `sanity`, `status`, `start`, `stop`, `logs`, `attach`, `health`, `probe`

### Export de preuves documentaires

```bash
bash modules/evidence_openclaw/scripts/cmd.sh status
bash modules/evidence_openclaw/scripts/cmd.sh export-docs
bash modules/evidence_openclaw/scripts/cmd.sh show-files
```

Sortie : `<workspace>/docs_evidence/openclaw_current_state/`
Fichiers produits :
- `01_doctor_status.txt`
- `02_configure_status.txt`
- `03_doctor_quick.txt`
- `04_workspace_context.txt`

### Hermes/OpenClaw

Le bridge Hermes/OpenClaw est mentionné comme preuve minimale close dans `HERMES_OPENCLAW_BRIDGE_CASE_01_V1.md` et `HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md`. Ce bridge n'est pas généralisé. Il reste borné au cas 01.

## Non périmètre

Ce document établit explicitement ce que le repo **ne prouve pas** :

- Pas de serving exposé
- Pas de cloud GPU actif
- Pas de framework bridge généralisé au-delà du cas 01
- Pas de runtime multi-machine hors `db-layer`
- Pas de mutation automatique de la config live OpenClaw
- Pas de migration runtime vers le repo `openclaw` (doc/gouvernance-only)

## ETABLI

Ce qui est prouvé par les docs et scripts lus :

- `menu_openclaw` donne accès aux menus des modules registry
- `model_provider_openclaw` lit la policy providers et la matrice agent→provider
- `configure_openclaw` expose config validate, agents list, dashboard
- `doctor_openclaw` expose doctor, health, probe, logs
- `evidence_openclaw` exporte les preuves runtime
- `gateway_openclaw` pilote le gateway local via tmux sous `openclaw`
- La chaîne install → config → gateway → doctor → evidence est documentée dans `GO_OPENCLAW_CHAIN_03.md`
- La policy provider est documentée dans `GO_OPENCLAW_PROVIDER_POLICY_04.md`

## NON ETABLI

Ce que le repo ne prove pas :

- Pas de bridge Hermes fonctionnel au-delà du cas 01 borné
- Pas de orchestration automate multi-modules
- Pas de sync automatique documentée entre modules
- Pas de workflow CI/CD OpenClaw
- Pas de monitoring temps réel
- Pas de rollback automate de la config runtime

## Point de reprise suivant

Par défaut : conserver la position documentaire actuelle sans ouvrir de GO supplémentaire.

N'ouvrir un GO state-dir, alignment patch ou bridge case 02 que sur besoin opératoire réel et vérifiable.

Les références documentaires à conserver :
- `GO_OPENCLAW_CHAIN_03.md` — chaîne standard
- `GO_OPENCLAW_PROVIDER_POLICY_04.md` — policy provider/model
- `GO_OPENCLAW_EVIDENCE_01.md` — export preuves