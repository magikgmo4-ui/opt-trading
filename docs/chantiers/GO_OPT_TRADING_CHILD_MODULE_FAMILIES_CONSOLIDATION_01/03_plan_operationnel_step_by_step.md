---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - modules
  - consolidation
  - plan
  - steps
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/01_liste_modules.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/02_ensembles_a_consolider.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/04_step_02_hygiene_documentaire_batch1.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/05_step_02_hygiene_documentaire_batch2_openclaw.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/06_step_02_hygiene_documentaire_batch3_core.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/07_step_02_hygiene_documentaire_batch4_verticales.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/08_step_03_family_decision_bot_vision.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/09_step_03_family_decision_deepseek.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/10_step_03_family_decision_reseau_ssh.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/11_step_03b_consolidation_eval_reseau_share_transfer.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/12_step_03_family_decision_desk.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/13_step_04_role_map_desk_pro.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/14_step_04_role_map_deepseek_student.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/15_step_04_role_map_reseau_share_transfer.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/16_step_05_family_plan_registry_ui_navigation.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/17_step_05_family_plan_openclaw.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/18_step_05_family_plan_collectors_market_intelligence.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/19_step_05_family_plan_vision.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/20_step_06_family_contracts_engine_pipeline.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/21_step_06_family_contracts_runtime_edge_platform.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/22_step_06_family_contracts_repo_tooling_authoring.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/91_synthese_resultats.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/92_plans_execution_sous_lots.md
  - docs/status/desk_pro_stack_canonique.md
  - docs/status/deepseek_student_canonique.md
  - docs/status/reseau_ssh_canonique.md
  - docs/status/bot_vision_canonique.md
  - docs/status/workflow_post_change_canonique.md
---

# Plan operationnel step-by-step

## Regle
Ce plan est volontairement conservateur :
- pas de move physique avant clarification des callers et du survivant par famille
- chaque step doit produire une preuve, une decision et un rollback

## Step 00 — baseline inventaire
- statut : complete
- objectif : figer la liste reelle des modules et la couverture `README`
- preuve :
  - [01_liste_modules.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/01_liste_modules.md)
- sortie :
  - `85` modules
  - `58` avec `README`
  - `27` sans `README`

## Step 01 — figer les ensembles
- statut : complete
- objectif : separer familles a consolider, familles a coordonner et surfaces a laisser separees
- preuve :
  - [02_ensembles_a_consolider.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/02_ensembles_a_consolider.md)

## Step 02 — hygiene documentaire minimale
- statut : complete
- objectif : rendre les familles actives lisibles avant toute action plus forte
- scope prioritaire :
  - `desk_pro`
  - `desk_common`
  - `deepseek_response`
  - `deepseek_thinking`
  - famille `openclaw*`
  - `auth`, `env`, `health`, `perf`, `router`, `webhook`, `workflow_post_change_v2`
- action attendue :
  - ajouter ou completer les `README`
  - expliciter role, entrypoints, dependances, survivant/transition si la famille est ambigue
- preuve observee (batch 1) :
  - [04_step_02_hygiene_documentaire_batch1.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/04_step_02_hygiene_documentaire_batch1.md)
  - couverture `README` passee de `58/85` a `69/85`
  - modules sans `README` restants : `16`
- preuve observee (batch 2 OpenClaw) :
  - [05_step_02_hygiene_documentaire_batch2_openclaw.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/05_step_02_hygiene_documentaire_batch2_openclaw.md)
  - couverture `README` passee de `69/85` a `76/85`
  - modules sans `README` restants : `9`
- preuve observee (batch 3 core wrappers) :
  - [06_step_02_hygiene_documentaire_batch3_core.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/06_step_02_hygiene_documentaire_batch3_core.md)
  - couverture `README` passee de `76/85` a `80/85`
  - modules sans `README` restants : `5`
- preuve observee (batch 4 verticales specialisees) :
  - [07_step_02_hygiene_documentaire_batch4_verticales.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/07_step_02_hygiene_documentaire_batch4_verticales.md)
  - couverture `README` passee de `80/85` a `85/85`
  - modules sans `README` restants : `0`
- reste a faire :
  - aucun
- rollback :
  - revert doc-only

## Step 03 — figer les survivants / transition / compatibilite
- statut : complete
- objectif : ne plus laisser de familles step-by-step sans statut operatoire clair
- familles cibles :
  - `deepseek*`
  - `reseau_ssh*`
  - `bot_vision*`
  - `desk_pro*` / `desk_*`
- action attendue :
  - confirmer survivant, transition, legacy, compat
  - aligner les docs courtes `docs/status/*` avec les README modules
- preuve observee (famille `bot_vision*`) :
  - [08_step_03_family_decision_bot_vision.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/08_step_03_family_decision_bot_vision.md)
  - paire operatoire transitoire fixee : `vision_bot` + `bot_vision_step2`
  - `bot_vision` reclasse en verticale historique `step1`
- preuve observee (famille `deepseek*`) :
  - [09_step_03_family_decision_deepseek.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/09_step_03_family_decision_deepseek.md)
  - verite runtime actuelle confirmee hors `modules/` : `scripts/student/`
  - candidat module unifie fixe : `deepseek_hub`
  - `deepseek_response` / `deepseek_thinking` maintenus en compatibilite
  - `deepseek_student` confirme comme transition non runtime
- preuve observee (famille `reseau_ssh*`) :
  - [10_step_03_family_decision_reseau_ssh.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/10_step_03_family_decision_reseau_ssh.md)
  - survivant confirme : `reseau_ssh_step2`
  - transition / prerequis confirme : `reseau_ssh_step1b`
  - legacy confirme : `reseau_ssh`
  - separation de lignee fixee par rapport a `shared*` et `winscp_transfer`
- preuve observee (step 03b - evaluation de suite) :
  - [11_step_03b_consolidation_eval_reseau_share_transfer.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/11_step_03b_consolidation_eval_reseau_share_transfer.md)
  - consolidation documentaire de suite recommandee
  - fusion physique non recommandee dans ce lot
- preuve observee (famille `desk_*`) :
  - [12_step_03_family_decision_desk.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/12_step_03_family_decision_desk.md)
  - stack multi-composants confirmee, sans survivant unique
  - roles fixes : `desk_pro`, `desk_pro_runner`, `desk_pro_orchestrator`, `desk_pro_dashboard`, `desk_common`
  - satellites adjacents distingues : `desk_snapshot_ingest`, `desk_capture_inputs`, `desk_analyze`, `desk_state`, `desk_retention`
- preuve attendue :
  - decision explicite par famille
- rollback :
  - revert doc-only

## Step 04 — suites P1
- statut : complete
- objectif : produire les cartes de role et frontieres des familles prioritaires
- familles :
  - `Desk Pro`
  - `DeepSeek/student`
  - `reseau/share/transfer`
- action attendue :
  - carte composants
  - entrypoint canonique
  - satellites
  - points de duplication
  - risques de consolidation
- preuve observee (suite `Desk Pro`) :
  - [13_step_04_role_map_desk_pro.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/13_step_04_role_map_desk_pro.md)
  - hierarchie d'entrypoints figee :
    - `menu-ops_menu_hub`
    - `scripts/admin_trading/desk_pro_cmd.sh`
    - `cmd-desk_pro_runner`
  - frontieres P1 confirmees entre coeur produit, facade operatoire, pipeline, rendu et support minimal
- preuve observee (suite `DeepSeek/student`) :
  - [14_step_04_role_map_deepseek_student.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/14_step_04_role_map_deepseek_student.md)
  - runtime actuel confirme : `scripts/student/`
  - facade module candidate confirmee : `deepseek_hub`
  - compatibilites maintenues : `deepseek_response`, `deepseek_thinking`
- preuve observee (suite `reseau/share/transfer`) :
  - [15_step_04_role_map_reseau_share_transfer.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/15_step_04_role_map_reseau_share_transfer.md)
  - baseline, surface canonique et modes d'acces specialises distingues
  - aucun move physique autorise dans ce lot
- rollback :
  - aucun si analyse seule

## Step 05 — suites P2
- statut : complete
- objectif : traiter les familles importantes mais moins urgentes
- familles :
  - `Registry/UI/navigation`
  - `Openclaw`
  - `Collectors / market intelligence`
  - `Vision`
- action attendue :
  - distinguer ce qui doit etre harmonise, mutualise, ou laisser separe
- preuve observee (suite `Registry/UI/navigation`) :
  - [16_step_05_family_plan_registry_ui_navigation.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/16_step_05_family_plan_registry_ui_navigation.md)
  - `registry/` confirme comme source de verite declarative
  - `localcms` qualifie comme consumer UI externe eventuel, non absorbable dans ce lot
- preuve observee (suite `Openclaw`) :
  - [17_step_05_family_plan_openclaw.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/17_step_05_family_plan_openclaw.md)
  - chaine fixee :
    - `install_module_openclaw`
    - `model_provider_openclaw`
    - `openclaw_config_modulaire`
    - `configure_openclaw`
    - `gateway_openclaw`
    - `doctor_openclaw`
    - `evidence_openclaw`
- preuve observee (suite `Collectors / market intelligence`) :
  - [18_step_05_family_plan_collectors_market_intelligence.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/18_step_05_family_plan_collectors_market_intelligence.md)
  - `collectors_core` confirme comme fondation partagee
  - separation explicite entre collecte, facade `marketdata` et intelligence aval
- preuve observee (suite `Vision`) :
  - [19_step_05_family_plan_vision.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/19_step_05_family_plan_vision.md)
  - paire operatoire transitoire relue sans figer un survivant unique
  - prochain besoin pointe vers une spec cross-platform ou une decision de survivant
- rollback :
  - aucun si analyse seule

## Step 06 — contrats plutot que fusion
- statut : complete
- objectif : durcir les familles a garder separees
- familles :
  - `Engine pipeline`
  - `Runtime edge / platform`
  - `Repo / tooling / authoring`
- action attendue :
  - normaliser contracts, wrappers, ownership, README
  - ne pas lancer de fusion physique
- preuve observee (famille `Engine pipeline`) :
  - [20_step_06_family_contracts_engine_pipeline.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/20_step_06_family_contracts_engine_pipeline.md)
  - ordre de pipeline reafirme via `desk_pro_orchestrator`
  - `engines` confirme comme coordination legere, pas megamodule
- preuve observee (famille `Runtime edge / platform`) :
  - [21_step_06_family_contracts_runtime_edge_platform.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/21_step_06_family_contracts_runtime_edge_platform.md)
  - frontieres fixees entre `env`, `auth`, `modules/webhook`, `webhook_server.py`, `perf/perf_app.py`, facades shell et `shared`
- preuve observee (famille `Repo / tooling / authoring`) :
  - [22_step_06_family_contracts_repo_tooling_authoring.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/22_step_06_family_contracts_repo_tooling_authoring.md)
  - sous-roles explicites entre audit, validation, hygiene repo, install, authoring et post-change
- rollback :
  - revert doc-only si modification documentaire

## Step 07 — moves physiques a faible risque seulement
- statut : conditional
- objectif : n'autoriser que les consolidations prouvees sans casse
- preconditions :
  - survivant confirme
  - callers verifies
  - rollback explicite
  - docs et wrappers mis a jour
- exemples potentiels :
  - reclassement de modules purement compat
  - mutualisation de scripts/doc dans une suite deja figee

## Step 08 — closeout ou sous-lots d'execution
- statut : complete
- objectif : decider si ce child reste un plan, ou devient parent d'execution par famille
- sous-lots d'execution recommandes si besoin :
  - `DESK_PRO_STACK_CONSOLIDATION`
  - `DEEPSEEK_FAMILY_CONSOLIDATION`
  - `RESEAU_SHARE_TRANSFER_CONSOLIDATION`
  - `OPENCLAW_FAMILY_CONSOLIDATION`
  - `VISION_FAMILY_SURVIVOR_DECISION`
- decision retenue :
  - `Step 07` n'est pas declenche dans ce child
  - aucun move faible risque n'est suffisamment prouve a l'echelle globale de `modules/`
  - le child est clos comme baseline de planification / consolidation
  - l'execution repart ensuite par sous-lots bornes
- preuve observee :
  - [90_closeout.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/90_closeout.md)
  - [91_synthese_resultats.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/91_synthese_resultats.md)
  - [92_plans_execution_sous_lots.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/92_plans_execution_sous_lots.md)

## Ordre recommande
1. hygiene `README` sur les modules actifs et ambigus
2. families `Desk Pro`, `DeepSeek`, `reseau_ssh`
3. suites `Registry/UI`, `Openclaw`, `Collectors`
4. `Vision`
5. conventions `engines` / `runtime edge` / `repo tooling`
6. seulement ensuite, moves physiques

## Resultat attendu
Au terme de ce plan, `modules/` doit devenir lisible par suites, sans remettre en cause les modules encore actifs ni casser les wrappers.

## Point de reprise
Le child est clos comme baseline.
Point de reprise recommande :
- `docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/92_plans_execution_sous_lots.md`
- ouvrir ensuite un sous-lot d'execution borne plutot que prolonger ce child

## RISKS

- À qualifier.
