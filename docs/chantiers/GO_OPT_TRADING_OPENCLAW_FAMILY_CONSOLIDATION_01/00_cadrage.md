---
doc_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01_CADRAGE
doc_type: chantier_child
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - openclaw
  - consolidation
  - wrappers
  - runbook
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/17_step_05_family_plan_openclaw.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/92_plans_execution_sous_lots.md
  - docs/product_targets/OPENCLAW_TARGET_CANON.md
  - docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/01_cartographie_suite.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/02_plan_operationnel_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/03_step_01_matrice_wrappers.md
---

# GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01

## Objet
Prendre la suite `OpenClaw` comme sous-lot d'execution borne, puis produire :
- une cartographie unique de la suite
- une matrice reelle des wrappers et verbes exposes
- un plan de convergence doc/wrappers
- une decision explicite sur ce qui reste separe, ce qui peut etre harmonise, et ce qui ne doit pas bouger

## Contexte
- le child `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` est clos comme baseline de planification
- `OpenClaw` y a ete retenu comme premier sous-lot d'execution prioritaire
- le role produit est deja borne :
  - cockpit local sur `db-layer`
  - non plateforme generale
  - non runtime critique transverse

## Portee
- suite `OpenClaw` uniquement :
  - `install_module_openclaw`
  - `model_provider_openclaw`
  - `openclaw_config_modulaire`
  - `configure_openclaw`
  - `gateway_openclaw`
  - `doctor_openclaw`
  - `evidence_openclaw`
  - `menu_openclaw`

## Anti-cibles
- pas de fusion physique immediate
- pas de migration vers un repo `openclaw` dedie
- pas d'extension multi-machine
- pas de requalification en produit user-facing
- pas de patch runtime sans preuve caller-level

## Cible finale
Disposer d'une suite `OpenClaw` lisible comme cockpit local borne, avec :
- un chainage explicite `install -> policy -> config structurelle -> config live -> gateway -> doctor -> evidence`
- des wrappers coherents et documentes
- un runbook de suite unique
- une decision finale :
  - closeout doc-only
  - ou petit lot shell/wrapper cible a faible risque

## Etabli
- `8` modules `OpenClaw` sont observes sous `modules/`
- les `8` modules exposent `scripts/cmd.sh`, `scripts/menu.sh` et `scripts/sanity.sh`
- les `8` modules exposent aussi un `scripts/install_shortcuts.sh`, mais la methode d'installation des shortcuts n'est pas uniforme
- les callers repo observes sont surtout internes a la suite :
  - `evidence_openclaw` appelle `cmd-doctor_openclaw` et `cmd-configure_openclaw` si disponibles
  - `menu_openclaw` depend de la registry `install_module_openclaw`
- aucun caller repo large ne prouve aujourd'hui un move physique global de la suite

## Livrables de ce lot
- [01_cartographie_suite.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/01_cartographie_suite.md)
- [02_plan_operationnel_step_by_step.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/02_plan_operationnel_step_by_step.md)
- [03_step_01_matrice_wrappers.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/03_step_01_matrice_wrappers.md)

## Point de reprise
Lire d'abord `01_cartographie_suite.md`, puis `03_step_01_matrice_wrappers.md`, puis derouler `02_plan_operationnel_step_by_step.md`.
