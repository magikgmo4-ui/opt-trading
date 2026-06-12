---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_CADRAGE
doc_type: chantier_child
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - modules
  - familles
  - consolidation
  - inventory
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/12_synthese_bloc_b_runtime.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/97_step_06_verification_zones_grises.md
  - registry/modules_registry.yaml
  - docs/status/desk_pro_stack_canonique.md
  - docs/status/deepseek_student_canonique.md
  - docs/status/reseau_ssh_canonique.md
  - docs/status/bot_vision_canonique.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/01_liste_modules.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/02_ensembles_a_consolider.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
---

# GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01

## Objet
Prendre la surface `modules/` comme lot a part entiere, produire :
- la liste complete des modules observes
- les ensembles coherents de modules
- les candidats reels a consolidation
- un plan operationnel step-by-step avant tout move physique

## Contexte
- le parent `GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01` a deja etabli que `modules/` est la surface durable la plus dense du repo
- cette surface melange produit, support runtime, readers, wrappers specialises, satellites machine et familles step-by-step
- l'objectif du present lot n'est pas de refactorer immediatement `modules/`, mais de figer un plan defensable

## Portee
- `modules/` uniquement
- appui sur `registry/modules_registry.yaml`
- recroisement avec les fiches statut deja existantes pour `desk_pro_stack`, `deepseek_student`, `reseau_ssh`, `bot_vision`

## Anti-cibles
- pas de fusion physique opportuniste dans ce lot
- pas de renommage de module sans audit de callers
- pas de reouverture globale des index de continuite dans ce lot

## Cible finale
Disposer d'un dossier enfant qui permette ensuite d'executer les consolidations famille par famille, sans repartir d'un audit brut.

## Etabli
- `modules/` contient `85` repertoires modules au `2026-04-24`
- `58` modules ont un `README.md`
- `27` modules n'ont pas de `README.md`
- plusieurs familles ont deja un statut documentaire court, mais pas encore un plan d'execution de consolidation

## Livrables de ce lot
- [01_liste_modules.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/01_liste_modules.md)
- [02_ensembles_a_consolider.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/02_ensembles_a_consolider.md)
- [03_plan_operationnel_step_by_step.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md)

## Point de reprise
Lire d'abord `01_liste_modules.md`, puis `02_ensembles_a_consolider.md`, puis derouler `03_plan_operationnel_step_by_step.md`.

## RISKS

- À qualifier.
