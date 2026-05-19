---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_05_OPENCLAW
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-05
  - openclaw
  - family-plan
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/product_targets/OPENCLAW_TARGET_CANON.md
  - docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md
  - modules/configure_openclaw/README.md
  - modules/doctor_openclaw/README.md
  - modules/evidence_openclaw/README.md
  - modules/gateway_openclaw/README.md
  - modules/install_module_openclaw/README.md
  - modules/menu_openclaw/README.md
  - modules/model_provider_openclaw/README.md
  - modules/openclaw_config_modulaire/README.md
---

# Step 05 - family plan `Openclaw`

## Statut
Complete.

## Objet
Figer la structuration P2 de la suite `Openclaw` comme cockpit operateur local borne, sans la requalifier en plateforme generale ni en runtime critique transversal.

## Verifications utilisees
- lecture de `docs/product_targets/OPENCLAW_TARGET_CANON.md`
- lecture de `docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md`
- lecture des README de :
  - `modules/configure_openclaw`
  - `modules/doctor_openclaw`
  - `modules/evidence_openclaw`
  - `modules/gateway_openclaw`
  - `modules/install_module_openclaw`
  - `modules/menu_openclaw`
  - `modules/model_provider_openclaw`
  - `modules/openclaw_config_modulaire`

## Carte de suite
| Couche | Surface retenue | Role |
|---|---|---|
| hub de reprise | `menu_openclaw` | federation et navigation de la suite |
| installation | `install_module_openclaw` | distribution locale des modules OpenClaw |
| politique provider/model | `model_provider_openclaw` | matrice de providers et modeles autorises |
| configuration structurelle | `openclaw_config_modulaire` | apply safe, validation, rollback |
| configuration live | `configure_openclaw` | facade operateur sur la config active |
| runtime local | `gateway_openclaw` | pilotage du gateway via `tmux` |
| diagnostic | `doctor_openclaw` | verification / repair-safe / probes |
| preuves | `evidence_openclaw` | export de preuves et prompt documentaire |

## Frontieres retenues
- `menu_openclaw` reste un hub de reprise. Il ne doit pas reimplementer les sous-modules.
- `install_module_openclaw` reste specialise OpenClaw. Il ne doit pas etre confondu avec `install_module`.
- `openclaw_config_modulaire` porte la securite structurelle de config. Il ne doit pas etre reduit a une simple facade UX.
- `configure_openclaw` porte l'usage operateur de la config live, au-dessus de `openclaw_config_modulaire`.
- `gateway_openclaw` reste le runtime local explicite. `doctor_openclaw` ne doit pas l'absorber.
- `evidence_openclaw` reste une couche de preuve et de continuite documentaire, distincte du runtime.
- `model_provider_openclaw` reste la couche de policy provider/model, distincte de la config machine et du gateway.

## Ce qui doit etre harmonise
- chainage explicite install -> policy -> config -> gateway -> doctor -> evidence
- conventions de wrappers `cmd/menu/sanity`
- cross-links docs et runbooks entre les huit modules
- terminologie commune autour de `db-layer`, cockpit local, provider policy, gateway health

## Ce qui peut etre mutualise plus tard
- helpers shell communs entre `configure_openclaw`, `doctor_openclaw` et `gateway_openclaw`
- conventions d'export d'evidence et de status
- petit registre de suite central si la duplication documentaire continue de croitre

## Ce qui doit rester separe
- policy provider/model et pilotage runtime
- configuration structurelle et facade operateur
- diagnostic et preuves documentaires
- hub de reprise et logique des sous-modules

## Risques a eviter
- fusionner `configure_openclaw` avec `openclaw_config_modulaire` et perdre la distinction structurel / live UX
- fusionner `doctor_openclaw` avec `gateway_openclaw` et melanger diagnostic et pilotage runtime
- promouvoir `evidence_openclaw` comme module runtime
- requalifier la suite en produit user-facing ou en plateforme multi-machine hors borne `db-layer`

## Decision retenue
- oui a une consolidation documentaire de suite `Openclaw`
- non a une fusion physique dans ce lot
- la suite reste bornee comme cockpit local `db-layer`
- prochain sous-lot logique si besoin :
  - `OPENCLAW_FAMILY_CONSOLIDATION`
  - ou un petit lot de conventions wrappers / docs sans impact runtime

## Rollback
- revert doc-only de cette note
- revert doc-only du plan si besoin

## Point de reprise
Suite P2 `Openclaw` cadree. Basculer sur `Collectors / market intelligence` puis `Vision`.
