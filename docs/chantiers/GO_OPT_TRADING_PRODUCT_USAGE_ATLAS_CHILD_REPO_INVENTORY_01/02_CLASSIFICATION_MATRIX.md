---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01_CLASSIFICATION_MATRIX
doc_type: classification_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/01_REPO_PRODUCT_CANDIDATES.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# 02_CLASSIFICATION_MATRIX - Classification des candidats

## Matrice de classification

| Surface / produit candidat | Type | Role final prevu | Usage actuel prouve | Bucket usage propose | Sources canoniques | Gap restant | NEXT_GO ou condition d'ouverture | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Desk Pro | Produit (stack multi-composants) | Pipeline operationnel desk : capture, analyse, execution, visualisation | Stack operationnelle avec runbooks, wrappers, script admin reel, dashboard | `USABLE_LIMITED` | `docs/status/desk_pro_stack_canonique.md`<br>`docs/desk_pro_multi_machine_quick_reference.md`<br>`docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md` | Survivant unique non fige. Frontiere desk_pro / desk_* en cours de clarification. | `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` (reprise existante) | ADD_TO_ATLAS |
| Bot Vision | Produit (pipeline vision multi-modules) | Pipeline capture screenshot -> analyse Vision -> artefacts Desk Pro / Telegram | Chaine transitoire active : `vision_bot` + `bot_vision_step2` | `USABLE_LIMITED` | `docs/status/bot_vision_canonique.md`<br>`docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`<br>Branches admin-trading BOT_VISION, HEADLESS | Pas de survivant unique. Transition step2 encore en cours de stabilisation. | `VISION_FAMILY_SURVIVOR_DECISION` ou poursuite consolidation existante | ADD_TO_ATLAS |
| Trading Dual Stack V1 / XAUUSD | Produit (framework trading) | Framework LAB/REALTIME unifie, perimetre XAUUSD borne | Schemas/config V1 etablis. LAB operationnel, comparateur operationnel, REALTIME minimale posee. V1 close. | `DOC_ONLY` | `docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md` | Sans broker, sans ordre reel, sans auto-trading. V1 close mais bornee. | `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` (seulement si extension reelle) | ADD_TO_ATLAS |
| TradingView / Telegram Alert Pipeline | Produit (pipeline d'alertes) | Reception alertes TradingView -> webhook -> observation -> Telegram | Parent observer merged (PR #200). Alert webhook en continuite active (PR #203). Dry-run bridge packet fonctionnel. | `USABLE_LIMITED` | `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`<br>`docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/90_CLOSEOUT.md` | Alert webhook non ferme. Export reel et integration Telegram a consolider. | Poursuite GO alert webhook actif puis closeout continuite | ADD_TO_ATLAS |
| OpenClaw Runtime | Produit (runtime d'orchestration IA) | Orchestration IA controlee au-dessus des surfaces trading | Modules installables, gateway, configuration. Cartographie doc (77 sources). TMUX supervision runtime en cours. | `USABLE_LIMITED` | `docs/product_targets/OPENCLAW_TARGET_CANON.md`<br>`docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/` | Orchestration runtime en construction. Agents non deployes. Synthese unifiee absente. | `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` (en cours) | ADD_TO_ATLAS |
| LocalCMS | Produit (UI consommatrice externe) | Consumer UI de opt-trading exploitant /shared | Cadrage et plan documentes. GO consumer parent ouvert. | `DOC_ONLY` | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/`<br>`docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/` | Projet externe, pas de runtime integre. Usage reel a prouver. | `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` puis preuve d'usage reel | ADD_TO_ATLAS |
| derivates_collector | Module produit (collecteur canonique) | Collecteur canonique de donnees marches derives, compatible famille collector | Module operationnel (V3->V13). Convergence doctrinale en cours. | `USABLE_LIMITED` | `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`<br>`docs/COLLECTORS_MIGRATION_MAP_01.md` | Convergence doctrinale en cours (phases 0-5). Artifacts, vocabulaire, config a aligner. | `GO_COLLECTORS_BASELINE_INVENTORY_01` | ADD_TO_ATLAS |
| derivates_analyzer | Module produit (analyse) | Analyse structuree et export des donnees derivatives_collector | Module present, connecte au collector. Preuve d'usage moins documentee. | `DOC_ONLY` | `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md`<br>`docs/ui_indexation/02_ui_registry_wrappers.md` | Preuve d'usage explicite manquante. | Documenter usage avant promotion | KEEP_CANDIDATE |
| probability_engine | Module (moteur d'analyse) | Synthese probabiliste pour le trading | Module present. Wrapper cmd existant. Preuve d'usage produit limitee. | `DOC_ONLY` | `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md`<br>`docs/ui_indexation/02_ui_registry_wrappers.md` | Manque closeout, runbook ou preuve d'usage produit explicite. | Fournir preuve d'usage avant proposition Atlas | KEEP_CANDIDATE |
| risk_engine | Module (calcul risque) | Calcul de risque extrait du webhook | Module present. Preuve d'usage produit limitee. | `DOC_ONLY` | `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md`<br>`docs/ui_indexation/02_ui_registry_wrappers.md` | Preuve d'usage produit explicite manquante. | Fournir preuve d'usage avant promotion | KEEP_CANDIDATE |
| Deepseek Student | Produit (famille LLM cote student) | Interface LLM operationnelle pour la surface student | Runbook operateur existant. deepseek_hub facade module la plus avancee. Runtime dans scripts/student/. | `USABLE_LIMITED` | `docs/status/deepseek_student_canonique.md`<br>`docs/student_deepseek_runbook.md`<br>`docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md` | Survivant canonique final non fige. Transition deepseek_student incomplete. | `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` ou child dedie | KEEP_CANDIDATE |
| Collectors spot (CoinGecko, Binance) | Modules produit (collecteurs spot) | Collecteurs spot normalises sur collectors_core | Modules valides. Doctrine famille appliquee. | `USABLE_LIMITED` | `docs/COLLECTORS_FAMILY_DOCTRINE_01.md` | Subordonnes a la doctrine famille. Statuts individuels clairs. | Suivre migration map collector | KEEP_CANDIDATE |
| Simex Bitget Bridge | Module (bridge echange) | Bridge simulation/backtest Bitget | Presets, contrat d'unites, docs SIMEX. | `DOC_ONLY` | `docs/simex/SIMEX_PRESETS.md`<br>`docs/simex/SIMEX_UNITS_CONTRACT.md` | Preuve d'usage operateur systematique a confirmer. | Fournir preuve d'usage avant promotion | KEEP_CANDIDATE |
| Git Fleet Guard | Module (outillage Git) | Garde-fou Git multi-machine | Module documente avec runbook. | `ARCHIVE_ONLY` | `docs/git_fleet_guard_runbook.md`<br>`docs/git_fleet_guard_module_overview.md` | Outillage de support, pas un produit utilisateur final. | Pas de promotion | DO_NOT_PROMOTE |
| validated_prompt_factory | Module (outil operateur) | Generateur de prompts structures pour IDE/IA | Module present. PARTIEL (manque Registry + Wrapper). | `DOC_ONLY` | `docs/ot/trae/OT_OPS_01_AUDIT.md`<br>`docs/architecture/REPO_SURFACES_MAP.md` | Integration incomplete. | Completer registry + wrapper avant de considerer une entree Atlas | KEEP_CANDIDATE |
| market_scanner | Module produit (moteur de scanning) | Scanner de marches pour opportunites et setups | Module present, wrapper cmd. Mentionne dans ui_indexation et indexation_desk. | `DOC_ONLY` | `docs/ui_indexation/01_ui_registry_modules.md`<br>`docs/indexation_desk/01_inventory_modules.md` | Pas de closeout ou runbook dedie. | Documenter usage et sorties avant promotion. | KEEP_CANDIDATE |
| decision_engine | Module (moteur de decision) | Moteur de decision pour signaux et strategies | Module present, wrappers. Reference OT_SVC_01 comme ON-DEMAND. | `DOC_ONLY` | `docs/ot/trae/OT_SVC_01_CANONICAL_RUNTIME_MAP.md`<br>`docs/indexation_desk/01_inventory_modules.md` | Closeout ou runbook absent. Relation avec execution_engine floue. | Documenter avant promotion. | KEEP_CANDIDATE |
| execution_engine | Module (moteur d'execution) | Moteur d'execution pour ordres et operations | Module present, wrappers. Mentionne dans indexation_desk. | `DOC_ONLY` | `docs/indexation_desk/01_inventory_modules.md`<br>`docs/indexation_desk/02_inventory_menus.md` | Preuve d'usage produit explicite manquante. | Documenter avant promotion. | KEEP_CANDIDATE |
| journal_engine | Module (journalisation) | Journalisation structuree des evenements trading | Module present, wrappers. Mentionne dans ui_registry et indexation_desk. | `DOC_ONLY` | `docs/ui_indexation/01_ui_registry_modules.md`<br>`docs/indexation_desk/01_inventory_modules.md` | Preuve d'usage produit explicite manquante. | Documenter avant promotion. | KEEP_CANDIDATE |
| liquidation_analyzer | Module (analyse de liquidation) | Analyse des risques de liquidation | Module present, wrappers. Mentionne dans ui_registry et indexation_desk. | `DOC_ONLY` | `docs/ui_indexation/01_ui_registry_modules.md`<br>`docs/indexation_desk/01_inventory_modules.md` | Preuve d'usage produit explicite manquante. | Documenter avant promotion. | KEEP_CANDIDATE |
| opportunity_ranker | Module (classement d'opportunites) | Classement et priorisation des opportunites trading | Module present, wrappers. Mentionne dans indexation_desk. | `DOC_ONLY` | `docs/indexation_desk/01_inventory_modules.md`<br>`docs/indexation_desk/02_inventory_menus.md` | Preuve d'usage produit explicite manquante. | Documenter avant promotion. | KEEP_CANDIDATE |
| perf_engine | Module (moteur de performance) | Calcul et suivi de performance | Module prouve live (`cmd-perf_engine status` OK). Wrapper non declare en registry. | `USABLE_LIMITED` | `docs/ot/reports/OT_LIVE_01_REPORT.md`<br>`docs/ui_indexation/01_ui_registry_modules.md`<br>`docs/indexation_desk/01_inventory_modules.md` | Pas de closeout produit dedie. Wrapper absent du registry. | Ajouter registry + documenter usage. | KEEP_CANDIDATE |
| marketdata | Module (donnees de marche) | Gestion et distribution des donnees de marche | Module present. Mentionne dans ui_registry et indexation_desk. | `DOC_ONLY` | `docs/ui_indexation/01_ui_registry_modules.md`<br>`docs/indexation_desk/01_inventory_modules.md` | Preuve d'usage peu documentee. Role exact flou. | Documenter avant toute promotion. | KEEP_CANDIDATE |
| memory_bricks | Module de support (compaction derivee) | Compaction structuree pour reprise de session | Module documente en gouvernance. Pilote closeout PASS. Subordonne a la hierarchie produit. | `ARCHIVE_ONLY` | `docs/governance/MEMORY_BRICKS_MAPPING.md`<br>`docs/governance/REPO_ROLE.md`<br>`docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md` | Compaction derivee, pas un produit final. | Aucun | DO_NOT_PROMOTE |
| workflow_ai | Doctrine de processus (doc-only) | Doctrine gated d'execution IA (GO/STOP, gates, templates) | Reference dans starter pack, audits OT, closeouts. | `ARCHIVE_ONLY` | `workflow_ai/WORKFLOW.md`<br>`docs/ot/reports/OT_STARTERPACK_AUDIT_01_REPORT.md` | Doctrine de processus, pas un produit. | Aucun | DO_NOT_PROMOTE |
| deploy_module_multi_machine | Outillage de deploiement | Propagation multi-machine des modules | Outillage valide, wrappers operationnels. Documente. | `ARCHIVE_ONLY` | `docs/deploy_module_multi_machine_continuity.md`<br>`docs/ops_wrappers_source_layout_refresh_runbook.md` | Outillage de support, pas un produit. | Aucun | DO_NOT_PROMOTE |
| webhook_server.py | Runtime racine historique | Entrypoint webhook historique | Runtime actif. Reference REPO_ROOT_POLICY. | `ARCHIVE_ONLY` | `docs/governance/REPO_ROOT_POLICY.md` | Deja couvert par TradingView Pipeline. | Aucun | DO_NOT_PROMOTE |
| bitget_bridge.py | Shim legacy | Shim historique vers simex_bitget_bridge | Shim de compatibilite. Module canonique deja dans l'inventaire. | `ARCHIVE_ONLY` | `docs/governance/REPO_ROOT_POLICY.md` | Deja couvert par Simex Bitget Bridge. | Aucun | ARCHIVE_ONLY |
| hf_free_platform | Module (plateforme HF) | Interface Hugging Face gratuite | Aucune reference documentaire canonique. | `ARCHIVE_ONLY` | Presence dans `modules/` | Aucune preuve d'usage. | Aucun | DO_NOT_PROMOTE |
| mimo_open_observer | Module (observateur MIMO) | Observateur protocole MIMO | Aucune reference documentaire canonique. | `ARCHIVE_ONLY` | Presence dans `modules/` | Aucune preuve d'usage. | Aucun | DO_NOT_PROMOTE |
| kil_v1 | Module (role inconnu) | Inconnu | Module present sans documentation exploitable. | `UNKNOWN_NEEDS_RESCAN` | Presence dans `modules/` | Role et usage inconnus. | Investiguer avant decision. | UNKNOWN_NEEDS_RESCAN |
| workflow_post_change_v2 | Module (workflow) | Gestion workflow post-modification | Module present. Fiche statut canonique + script sanity. | `ARCHIVE_ONLY` | `docs/status/workflow_post_change_canonique.md`<br>`scripts/sanity_check_post_change_v2.sh` | Support operationnel, pas un produit final. | Aucun | DO_NOT_PROMOTE |
| Modules support (20) | Infrastructure technique | Voir liste dans 01b_ADDENDUM | Modules de support : env, health, auth, install_module, naming_normalizer, router, shared, shared_files_sftp, shared_sshfs_permanent, winscp_transfer, repo_hygiene, repo_local_artifacts, repo_ownership_guard, audit, dev_validation_hub, scripts, engines, trae_module_validator, ui_registry_msi, perf | `ARCHIVE_ONLY` | Presence dans `modules/` | Infrastructure technique, pas des produits. | Aucun | DO_NOT_PROMOTE |
| collectors_core | Fondation partagee (package) | Base runtime partagee pour modules collecteurs | Package valide, utilise par spot collectors. | `ARCHIVE_ONLY` | `docs/COLLECTORS_FAMILY_DOCTRINE_01.md` | Fondation partagee, pas un produit autonome. | Aucun | DO_NOT_PROMOTE |
| module_contextuals_shell | Module (support technique) | Coquille technique pour appels modules | Module present. Aucune preuve d'usage produit. | `ARCHIVE_ONLY` | Presence dans `modules/` | Aucun usage produit documente. | Pas de promotion | DO_NOT_PROMOTE |
| Ops wrappers / menus / registries | Modules de support (wrappers generiques) | Infrastructure de navigation et enregistrement des modules | Modules presents, utilises comme support. | `ARCHIVE_ONLY` | Presence dans `modules/` | Wrappers generiques, pas des produits utilisateur finaux. | Pas de promotion | DO_NOT_PROMOTE |
| Surfaces historiques | Historique | Aucun role produit actif | Surfaces gelees ou archivees. | `ARCHIVE_ONLY` | `docs/ot/trae/OT_OPS_05B_DESK_PRO_FREEZE_NOTE.md`<br>`_archive/` | Aucun. | Aucun | ARCHIVE_ONLY |

## Zones grises

Voir detail complet dans `01b_REPO_PRODUCT_CANDIDATES_ADDENDUM.md`.

| Zone | Description | Recommandation |
| --- | --- | --- |
| ZG-01 | Frontiere desk_pro vs desk_* non tranchee | Traiter comme stack Desk Pro unifiee |
| ZG-02 | Survivant unique Bot Vision non fige | Maintenir USABLE_LIMITED, NEXT_GO = VISION_FAMILY_SURVIVOR_DECISION |
| ZG-03 | kil_v1 role inconnu | UNKNOWN_NEEDS_RESCAN |
| ZG-04 | hf_free_platform et mimo_open_observer sans doc | DO_NOT_PROMOTE |
| ZG-05 | perf vs perf_engine vs perf_app.py | Traiter comme un seul produit perf_engine |
| ZG-06 | Recouvrement TradingView Pipeline et webhook_server.py | Deja couvert, pas de doublon |
| ZG-07 | Scripts hors modules (support operationnel) | Pas de nouvelle entree Atlas |

## Resume des decisions

| Decision | Nombre | Surfaces |
| --- | --- | --- |
| ADD_TO_ATLAS | 7 | Desk Pro, Bot Vision, Trading Dual Stack V1, TradingView/Telegram Alert Pipeline, OpenClaw Runtime, LocalCMS, derivatives_collector |
| KEEP_CANDIDATE | 16 | derivatives_analyzer, probability_engine, risk_engine, Deepseek Student, Collectors spot, Simex Bitget Bridge, validated_prompt_factory, market_scanner, decision_engine, execution_engine, journal_engine, liquidation_analyzer, opportunity_ranker, perf_engine, marketdata, + modules support non prouves |
| DO_NOT_PROMOTE / ARCHIVE_ONLY | 27 | Git Fleet Guard, module_contextuals_shell, Ops wrappers/menus/registries, surfaces historiques, memory_bricks, workflow_ai, deploy_module_multi_machine, webhook_server.py, bitget_bridge.py, hf_free_platform, mimo_open_observer, workflow_post_change_v2, collectors_core, + 20 modules de support |
| UNKNOWN_NEEDS_RESCAN | 1 | kil_v1 |

## RISKS

- À qualifier.
