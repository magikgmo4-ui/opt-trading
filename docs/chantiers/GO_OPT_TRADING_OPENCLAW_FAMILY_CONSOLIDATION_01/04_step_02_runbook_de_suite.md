---
doc_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01_STEP_02_RUNBOOK
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - openclaw
  - runbook
  - chain
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/02_plan_operationnel_step_by_step.md
  - modules/menu_openclaw/docs/RUNBOOK.txt
  - modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md
  - modules/model_provider_openclaw/docs/RUNBOOK.txt
  - modules/openclaw_config_modulaire/docs/README.md
  - modules/gateway_openclaw/docs/README.md
  - modules/configure_openclaw/docs/RUNBOOK.txt
  - modules/doctor_openclaw/docs/RUNBOOK.txt
  - modules/evidence_openclaw/docs/RUNBOOK.txt
---

# Step 02 - runbook de suite `OpenClaw`

## Statut
Complete.

## Objet
Produire un runbook unique de suite `OpenClaw` qui resolve les ecarts observes entre :
- la chaine documentee dans `menu_openclaw`
- le role `policy` de `model_provider_openclaw`
- l'ordre reel entre config, gateway, doctor et evidence

## Verifications utilisees
- lecture de `modules/menu_openclaw/docs/RUNBOOK.txt`
- lecture de `modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md`
- lecture de `modules/model_provider_openclaw/docs/RUNBOOK.txt`
- lecture de `modules/openclaw_config_modulaire/docs/README.md`
- lecture de `modules/gateway_openclaw/docs/README.md`
- lecture des runbooks locaux `configure_openclaw`, `doctor_openclaw`, `evidence_openclaw`

## Decision de chaine
Le runbook unique retient deux parcours distincts :

### 1. Reprise lecture
Parcours utilise pour relire l'etat sans modifier le systeme :
1. `menu_openclaw`
2. `model_provider_openclaw`
3. `configure_openclaw`
4. `gateway_openclaw`
5. `doctor_openclaw`
6. `evidence_openclaw`

### 2. Patch operatoire borne
Parcours utilise quand une action de config ou runtime est vraiment necessaire :
1. `install_module_openclaw`
2. `model_provider_openclaw`
3. `openclaw_config_modulaire`
4. `gateway_openclaw`
5. `configure_openclaw`
6. `doctor_openclaw`
7. `evidence_openclaw`

## Pourquoi cette distinction
- `menu_openclaw` est un hub de reprise, pas un maillon runtime
- `model_provider_openclaw` doit etre relu avant toute action structurelle ou live
- `openclaw_config_modulaire` reste la couche structurelle de backup/apply/rollback
- `configure_openclaw` reste la facade live, apres la policy et la structure
- `gateway_openclaw` doit etre verifie ou redemarre selon le cas, pas presume toujours actif
- `doctor_openclaw` valide apres la couche runtime
- `evidence_openclaw` reste la sortie de preuve finale

## Runbook unique retenu

### Phase A - reprise minimale lecture
```bash
cd /opt/trading
bash modules/menu_openclaw/scripts/sanity.sh
bash modules/menu_openclaw/scripts/cmd.sh status
bash modules/menu_openclaw/scripts/cmd.sh list-menus
```

### Phase B - lecture policy et etat local
```bash
sudo -iu openclaw
cd /opt/trading
bash modules/model_provider_openclaw/scripts/cmd.sh status
bash modules/model_provider_openclaw/scripts/cmd.sh show-agent orchestrateur
bash modules/configure_openclaw/scripts/cmd.sh status
bash modules/gateway_openclaw/scripts/cmd.sh status
bash modules/doctor_openclaw/scripts/cmd.sh status
```

### Phase C - changement borne si necessaire
```bash
sudo -iu openclaw
cd /opt/trading
bash modules/openclaw_config_modulaire/scripts/cmd.sh backup
bash modules/openclaw_config_modulaire/scripts/cmd.sh apply
bash modules/openclaw_config_modulaire/scripts/cmd.sh validate
bash modules/gateway_openclaw/scripts/cmd.sh start
bash modules/gateway_openclaw/scripts/cmd.sh health
bash modules/gateway_openclaw/scripts/cmd.sh probe
bash modules/configure_openclaw/scripts/cmd.sh validate
```

### Phase D - diagnostic et preuve
```bash
sudo -iu openclaw
cd /opt/trading
bash modules/doctor_openclaw/scripts/cmd.sh quick
bash modules/evidence_openclaw/scripts/cmd.sh export-docs
bash modules/evidence_openclaw/scripts/cmd.sh show-files
```

## Regles d'usage
- `model_provider_openclaw` est la porte de lecture de policy avant changement
- `openclaw_config_modulaire` est la seule couche structurelle de config
- `configure_openclaw` ne remplace pas `openclaw_config_modulaire`
- `doctor_openclaw` ne remplace pas `gateway_openclaw`
- `evidence_openclaw` clot le cycle ; il ne sert pas de check runtime primaire

## Ecarts resolus par Step 02
- la policy `model_provider_openclaw` est reintegree dans la chaine standard
- la distinction reprise lecture vs patch operatoire est explicite
- l'ordre `config structurelle -> gateway -> configure -> doctor -> evidence` est garde pour l'operatoire
- `menu_openclaw` est fixe comme entree de reprise, pas comme substitution des sous-modules

## Point de reprise
Step suivant :
- proposer la convention de wrappers de famille
- ne pas toucher aux scripts avant d'avoir fige les verbes communs et les verbes a write-scope eleve

## RISKS

- À qualifier.
