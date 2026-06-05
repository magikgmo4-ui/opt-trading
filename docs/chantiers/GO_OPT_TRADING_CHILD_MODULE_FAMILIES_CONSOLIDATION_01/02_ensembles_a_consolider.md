---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_ENSEMBLES
doc_type: chantier_family_map
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: active
lifecycle_stage: analysis
topic_keys:
  - opt-trading
  - modules
  - families
  - consolidation
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - modules/desk_pro_runner/README.md
  - modules/desk_pro_orchestrator/README.md
  - modules/deepseek_hub/README.md
  - modules/deepseek_student/README.md
  - modules/simex_bitget_bridge/README.md
  - modules/vision_bot/README.md
  - modules/reseau_ssh_step1b/README.md
  - modules/reseau_ssh_step2/README.md
  - docs/status/desk_pro_stack_canonique.md
  - docs/status/deepseek_student_canonique.md
  - docs/status/reseau_ssh_canonique.md
  - docs/status/bot_vision_canonique.md
---

# Ensembles a consolider

## Regle de lecture
- `P1` = consolidation a preparer en premier
- `P2` = structuration necessaire, mais apres les familles critiques
- `P3` = coordination utile ou clarification documentaire, sans urgence d'execution
- `consolider` ne veut pas dire `fusionner immediatement`

## P1 — Consolidation prioritaire

### 1. Desk Pro stack
Modules :
- `desk_pro_runner`
- `desk_pro_orchestrator`
- `desk_pro_dashboard`
- `desk_state`
- `desk_snapshot_ingest`
- `desk_retention`
- `desk_capture_inputs`
- `desk_analyze`
- `desk_common`
- `desk_pro`

Signal fort :
- `desk_pro_runner` se presente comme facade operateur de `desk_pro_orchestrator` et `desk_pro_dashboard`
- `desk_pro_orchestrator` decrit une pipeline multi-modules explicite
- `desk_state`, `desk_snapshot_ingest`, `desk_retention` gravitent deja autour du dashboard / stack Desk Pro
- `desk_common` et `desk_pro` sont des centres de gravite sans `README`
- la fiche [desk_pro_stack_canonique.md](/C:/Users/ghost/opt-trading/docs/status/desk_pro_stack_canonique.md) confirme une stack multi-composants encore a clarifier

Type de consolidation recommande :
- d'abord consolidation documentaire et contractuelle
- ensuite seulement rationalisation des frontieres `runner / orchestrator / dashboard / satellites`

Decision de lot :
- oui, famille prioritaire

### 2. DeepSeek / student runtime
Modules :
- `deepseek_hub`
- `deepseek_thinking`
- `deepseek_response`
- `deepseek_student`
- `perm_fix_student`

Signal fort :
- `deepseek_hub` indique explicitement qu'il corrige et unifie `deepseek_thinking` et `deepseek_response`
- `deepseek_student` indique explicitement qu'il n'est pas la source de verite runtime actuelle
- la fiche [deepseek_student_canonique.md](/C:/Users/ghost/opt-trading/docs/status/deepseek_student_canonique.md) confirme que le survivant final n'est pas encore fige

Type de consolidation recommande :
- d'abord figer la verite runtime entre `modules/deepseek_*`, `student/` et `scripts/student/`
- marquer `deepseek_thinking` et `deepseek_response` comme compat / legacy si confirme

Decision de lot :
- oui, famille prioritaire

### 3. Reseau / partage / transfert
Modules :
- `reseau_ssh`
- `reseau_ssh_step1b`
- `reseau_ssh_step2`
- `shared`
- `shared_files_sftp`
- `shared_sshfs_permanent`
- `winscp_transfer`

Signal fort :
- `reseau_ssh_step2` est deja documente comme survivant canonique
- `reseau_ssh_step1b` est documente comme prerequis intermediaire
- la fiche [reseau_ssh_canonique.md](/C:/Users/ghost/opt-trading/docs/status/reseau_ssh_canonique.md) fixe deja un survivant, une transition et un legacy
- `shared*` et `winscp_transfer` relevent de la meme capacite de transport / partage machine

Type de consolidation recommande :
- consolidation de lignee et de roles
- pas de fusion physique immediate
- clarifier ce qui releve de SSH, de partage monte, de SFTP et de transfert Windows

Decision de lot :
- oui, famille prioritaire

## P2 — Structuration necessaire

### 4. Registry / UI / navigation
Modules :
- `machines_registry_reader`
- `modules_registry_reader`
- `registry_meta_reader`
- `wrappers_registry_reader`
- `registry_router`
- `ui_registry_msi`
- `ops_menu_hub`
- `ops_super_menu`
- `ops_wrappers`

Signal fort :
- `registry_router` se decrit comme point d'entree unique vers les readers
- `ui_registry_msi` est une source de verite UI locale branchable sur `registry/ui_surfaces_registry.yaml`
- `ops_menu_hub` regroupe deja des wrappers par familles fonctionnelles

Type de consolidation recommande :
- consolidation de suite et de conventions
- shared base de lecture si duplication technique
- garder router / MSI / hub operateur comme entrypoints distincts

Decision de lot :
- oui, mais apres P1

### 5. Openclaw
Modules :
- `configure_openclaw`
- `doctor_openclaw`
- `evidence_openclaw`
- `gateway_openclaw`
- `install_module_openclaw`
- `menu_openclaw`
- `model_provider_openclaw`
- `openclaw_config_modulaire`

Signal fort :
- famille homogene par suffixe/prefixe
- forte densite de modules sans `README`
- topologie repetee `docs/`, `scripts/`, `app/`, `config/` deja visible

Type de consolidation recommande :
- d'abord cartographie et clarification des roles de sous-systeme
- ensuite mutualisation eventuelle des scripts / docs / config communes

Decision de lot :
- oui, mais apres P1

### 6. Collectors / market intelligence
Modules :
- `collector_binance_spot`
- `collector_coingecko`
- `derivatives_collector`
- `derivatives_analyzer`
- `market_scanner`
- `marketdata`
- `liquidation_analyzer`
- `opportunity_ranker`
- appui hors `modules/` : `packages/collectors_core`

Signal fort :
- `collector_binance_spot` et `collector_coingecko` consomment deja `packages/collectors_core`
- la doc repo-level collectors traite `collectors_core` comme fondation partagee
- `derivatives_collector` et les analyzers adjacents restent encore a articuler proprement avec cette fondation

Type de consolidation recommande :
- convergence selective vers `collectors_core`
- ne pas forcer de migration totale des modules derives sans preuve de valeur

Decision de lot :
- oui, apres P1

### 7. Vision family
Modules :
- `bot_vision`
- `bot_vision_step2`
- `vision_bot`

Signal fort :
- coexistence de nomenclature step et nom final
- la fiche [bot_vision_canonique.md](/C:/Users/ghost/opt-trading/docs/status/bot_vision_canonique.md) confirme qu'aucun survivant n'est encore fige
- `vision_bot` et `bot_vision_step2` ont tous deux une presence operatoire/documentaire

Type de consolidation recommande :
- d'abord decision de survivant
- ensuite seulement consolidation de wrappers et de docs

Decision de lot :
- oui, mais seulement apres clarification produit/runtime

## P3 — Coordination plus que fusion

### 8. Engine pipeline
Modules :
- `decision_engine`
- `execution_engine`
- `journal_engine`
- `perf_engine`
- `portfolio_engine`
- `position_engine`
- `probability_engine`
- `risk_engine`
- `engines`

Signal fort :
- `desk_pro_orchestrator` decrit deja leur ordre d'execution exact
- la valeur est dans les contrats entre modules, pas dans une fusion physique

Type de consolidation recommande :
- standardiser les contrats I/O, outputs de run, erreurs et points de reprise
- garder des modules separes

Decision de lot :
- coordination prioritaire, pas fusion

### 9. Repo / tooling / module authoring
Modules :
- `audit`
- `dev_validation_hub`
- `git_fleet_guard`
- `install_module`
- `module_contextuals_shell`
- `naming_normalizer`
- `repo_hygiene`
- `repo_local_artifacts`
- `repo_ownership_guard`
- `trae_module_validator`
- `validated_prompt_factory`
- `workflow_post_change_v2`

Signal fort :
- famille fonctionnelle large, mais pas mono-produit
- ces modules servent surtout l'operateur et la qualite repo

Type de consolidation recommande :
- harmonisation conventions, wrappers, README, ownership
- pas de fusion globale recommandee

Decision de lot :
- coordination seulement

### 10. Runtime edge / platform
Modules :
- `auth`
- `env`
- `health`
- `perf`
- `router`
- `scripts`
- `shared`
- `webhook`

Signal fort :
- modules fins de plateforme, souvent sans `README`
- valeur dans la clarte de role, pas dans une fusion aveugle

Type de consolidation recommande :
- documenter les roles et les contracts
- garder les surfaces separees

Decision de lot :
- coordination seulement

### 11. Verticales speciales a audit individuel
Modules :
- `hf_free_platform`
- `kil_v1`
- `mimo_open_observer`
- `simex_bitget_bridge`
- `trading_lab_v1`
- `trading_realtime_v1`

Signal fort :
- usages specialises, perimetres produit heterogenes
- pas de benefice evident a une consolidation transversale sans objectif produit commun

Decision de lot :
- laisser separes
- auditer individuellement si besoin

## Synthese
- les familles a traiter en premier sont `Desk Pro`, `DeepSeek/student`, `reseau/share/transfer`
- les familles `Registry/UI`, `Openclaw`, `Collectors`, `Vision` demandent une structuration, pas un rangement cosmetique
- les `engines`, le `runtime edge` et le `repo tooling` doivent surtout etre contractes et documentes

## Point de reprise
Derouler `03_plan_operationnel_step_by_step.md` en commençant par le lot `P1`.

## RISKS

- À qualifier.
