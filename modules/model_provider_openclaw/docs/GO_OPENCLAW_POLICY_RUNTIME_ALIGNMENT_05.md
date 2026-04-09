# GO_OPENCLAW_POLICY_RUNTIME_ALIGNMENT_05

## Classification

- Type : diagnostic ponctuel
- Statut : `READY`
- Portee : constat d alignement policy/runtime OpenClaw, sans modification runtime

## But

Consigner de maniere canonique l etat d alignement observable entre la policy `model_provider_openclaw` et le runtime OpenClaw relu sur `db-layer`, sans extrapolation.

## Repo canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## Source de verite retenue

Ce document part uniquement des lectures suivantes :

- `modules/model_provider_openclaw/scripts/sanity.sh`
- `modules/model_provider_openclaw/scripts/cmd.sh status`
- `modules/model_provider_openclaw/scripts/cmd.sh show-agent orchestrateur`
- `modules/model_provider_openclaw/scripts/cmd.sh show-agent reviewer`
- `modules/model_provider_openclaw/scripts/cmd.sh export-json`
- `modules/configure_openclaw/scripts/cmd.sh status`
- `modules/doctor_openclaw/scripts/cmd.sh status`
- `modules/evidence_openclaw/scripts/cmd.sh status`

## ETABLI

### Policy V1 lue

- `POLICY_VERSION = 1.0`
- `MATRIX_VERSION = 1.0`
- `DEFAULT_STRATEGY = deny_unlisted`
- providers autorises : `openai_compatible_local`, `openrouter`
- agents couverts par la policy V1 : `orchestrateur`, `builder`, `reviewer`, `lab`

### Runtime relu

- config runtime valide sur `~/.openclaw/openclaw.json`
- agents runtime visibles : `orchestrateur`, `builder`, `reviewer`, `lab`, `codexoauth`
- workspace observe : `/home/openclaw/.openclaw/workspace-orchestrateur`

### Alignements observes

- `orchestrateur`
  - policy primary : `openrouter / qwen/qwen3-32b`
  - runtime affiche : `openrouter/qwen/qwen3-32b`
  - constat : aligne

- `builder`
  - policy primary : `openrouter / qwen/qwen3-coder-30b-a3b-instruct`
  - runtime affiche : `openrouter/qwen/qwen3-coder-30b-a3b-instruct`
  - constat : aligne

### Ecarts observes

- `reviewer`
  - policy primary : `openrouter / deepseek/deepseek-r1`
  - runtime affiche : `openai/gpt-5.4`
  - constat : non aligne dans l etat observe

- `lab`
  - policy primary : `openai_compatible_local / qwen3:14b-instruct`
  - policy fallback : `openrouter / qwen/qwen3-14b`
  - runtime affiche : `openrouter/qwen/qwen3-14b`
  - constat : non aligne avec le primary observe ; correspond au fallback policy

- `codexoauth`
  - visible cote runtime
  - non present dans la policy V1 lue
  - constat : hors perimetre policy V1 observee

## NON ETABLI

- que la policy V1 soit deja appliquee automatiquement a la config live
- la cause exacte des ecarts observes sur `reviewer` et `lab`
- le statut cible de `codexoauth` dans la policy V1 courante

## RUNBOOK

Ce document n est pas un runbook de correction.

Lecture minimale :
- relire la policy via `model_provider_openclaw`
- relire le runtime via `configure_openclaw` et `doctor_openclaw`
- comparer uniquement les primary policy et les modeles runtime explicitement affiches
- ne pas lancer de correction depuis ce GO

## CHANGELOG

- `POLICY_RUNTIME_ALIGNMENT_05` : isolement documentaire des alignements et ecarts observes entre policy V1 et runtime OpenClaw
- aucun changement runtime
- aucune mutation de config

## Conditions de close

Le document est clos si et seulement si :
- les alignements observes sont distingues des ecarts observes
- `reviewer`, `lab` et `codexoauth` sont traites comme constats
- aucun plan de correction n est affirme sans GO complementaire

## Hors perimetre

- toute modification de `~/.openclaw/openclaw.json`
- tout changement de modele runtime
- toute integration automatique de la policy dans le runtime
- toute correction de `reviewer`, `lab` ou `codexoauth`
- tout commit runtime hors documentation

## Point de reprise suivant

Plus petit prochain pas utile :
- ouvrir un GO distinct seulement si une verification lecture-only supplementaire doit determiner si les ecarts `reviewer` et `lab`, ainsi que le cas `codexoauth`, relevent d un besoin d alignement operatoire.
