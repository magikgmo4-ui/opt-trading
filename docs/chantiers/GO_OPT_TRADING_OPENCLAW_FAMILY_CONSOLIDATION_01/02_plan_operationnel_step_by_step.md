---
doc_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - openclaw
  - plan
  - steps
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/01_cartographie_suite.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/03_step_01_matrice_wrappers.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/17_step_05_family_plan_openclaw.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/92_plans_execution_sous_lots.md
---

# Plan operationnel step-by-step

## Regle
Le sous-lot reste conservateur :
- pas de move physique sans callers verifies
- pas de fusion runtime sans rollback simple
- chaque step doit produire une preuve, une decision et une prochaine action claire

## Step 00 - baseline de suite
- statut : complete
- objectif : figer le scope exact du sous-lot `OpenClaw`
- preuve :
  - [00_cadrage.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/00_cadrage.md)
  - [01_cartographie_suite.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/01_cartographie_suite.md)
- sortie :
  - `8` modules
  - chainage de suite borne
  - anti-cibles explicites

## Step 01 - matrice des wrappers et verbes
- statut : complete
- objectif : cartographier les wrappers reels et les verbes exposes
- preuve :
  - [03_step_01_matrice_wrappers.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/03_step_01_matrice_wrappers.md)
- sortie :
  - invariants `sanity/status`
  - verbes specialises par module
  - ecarts de shortcuts et de naming identifies
- rollback :
  - revert doc-only

## Step 02 - runbook de suite unique
- statut : complete
- objectif : produire un runbook unique `OpenClaw` centre sur la chaine de reprise operateur
- action attendue :
  - aligner l'ordre `install -> policy -> config structurelle -> config live -> gateway -> doctor -> evidence`
  - distinguer lecture seule vs action explicite
  - fixer les entrees de reprise par cas d'usage
- preuve observee :
  - [04_step_02_runbook_de_suite.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/04_step_02_runbook_de_suite.md)
- sortie :
  - parcours `reprise lecture` fige
  - parcours `patch operatoire borne` fige
  - `model_provider_openclaw` reintegre comme gate de policy avant action
- rollback :
  - revert doc-only

## Step 03 - conventions de wrappers
- statut : complete
- objectif : proposer une convention de verbes coherente sans casser les sous-modules
- action attendue :
  - fixer les verbes de base obligatoires
  - fixer les verbes `show-*` / `export-*` / `paths`
  - qualifier les verbes write-scope eleve
  - distinguer hub, config, runtime, doctor, evidence
- preuve observee :
  - [05_step_03_conventions_wrappers.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/05_step_03_conventions_wrappers.md)
- sortie :
  - noyau commun `cmd/menu/sanity`
  - verbes de base et verbes a write-scope eleve figes
  - alias principal du hub fixe sur `menu-openclaw` / `cmd-openclaw`
- rollback :
  - revert doc-only

## Step 04 - audit de duplication et mutualisations legeres
- statut : complete
- objectif : verifier si une petite mutualisation shell/doc est justifiee
- action attendue :
  - comparer `install_shortcuts.sh`
  - comparer les patrons `cmd.sh`, `menu.sh`, `sanity.sh`
  - verifier la duplication de runbooks/docs de base
  - ne proposer que des mutualisations sans ambiguite
- preuve observee :
  - [06_step_04_audit_duplications.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/06_step_04_audit_duplications.md)
- sortie :
  - pas de duplication litterale assez forte pour mutualisation immediate
  - pas de helper shell commun justifie a ce stade
  - un futur patch ne pourrait etre que tres cible
- rollback :
  - revert doc-only ou revert petit patch shell cible

## Step 05 - decision d'execution
- statut : complete
- objectif : choisir la sortie du sous-lot
- options autorisees :
  - closeout doc-only si la structure suffit
  - petit patch shell/wrapper si le gain est prouve et le risque borne
  - ouverture d'un mini lot supplementaire si une anomalie runtime precise l'impose
- preuve observee :
  - [90_closeout.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/90_closeout.md)
- sortie :
  - closeout doc-only retenu
  - aucun patch shell publie
  - next sous-lot recommande : `GO_OPT_TRADING_RESEAU_SHARE_TRANSFER_CONSOLIDATION_01`
- rollback :
  - revert doc-only ou revert patch borne

## Ordre recommande
1. baseline et matrice wrappers
2. runbook de suite
3. conventions de wrappers
4. duplication / mutualisations
5. decision finale

## Resultat attendu
Au terme de ce plan, la suite `OpenClaw` doit etre pilotable comme cockpit local borne, sans ambiguite sur :
- le chainage des modules
- les verbes exposes
- les actions a risque
- les limites de consolidation

## Point de reprise
Prochaine action :
- lot clos
- point de reprise externe :
  - `docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/92_plans_execution_sous_lots.md`
  - puis `GO_OPT_TRADING_RESEAU_SHARE_TRANSFER_CONSOLIDATION_01`

## RISKS

- À qualifier.
