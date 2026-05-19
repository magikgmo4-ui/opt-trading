---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01_REPO_PRODUCT_CANDIDATES
doc_type: product_candidates
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md
  - docs/status/desk_pro_stack_canonique.md
  - docs/status/bot_vision_canonique.md
  - docs/status/deepseek_student_canonique.md
  - docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/GO_INDEX.md
---

# 01_REPO_PRODUCT_CANDIDATES - Inventaire des surfaces candidates

## Deja dans l'Atlas (socle initial)

Ces 6 produits sont deja classes et ne sont pas reinventories ici.

| Produit | Bucket |
| --- | --- |
| Repo KG | `USABLE_NOW` |
| ClickUp Cockpit | `USABLE_LIMITED` |
| Airtable Orchestration Layer | `DOC_ONLY` |
| Botpress Adapter | `SIMULATED_ONLY` |
| OpenClaw Docs Library | `DOC_ONLY` |
| BTC COIN-M Accumulation Engine | `FORBIDDEN_LIVE` |

---

## Candidat 01 -- Desk Pro (stack multi-composants)

| Champ | Valeur |
| --- | --- |
| **Nom** | Desk Pro |
| **Type** | Produit (stack multi-composants) |
| **Modules principaux** | `desk_pro`, `desk_pro_runner`, `desk_pro_orchestrator`, `desk_pro_dashboard`, `desk_common`, `desk_state`, `desk_analyze`, `desk_capture_inputs`, `desk_retention`, `desk_snapshot_ingest` |
| **Role final prevu** | Pipeline operationnel de capture, analyse, execution et visualisation desk trading. |
| **Usage actuel prouve** | Stack operationnelle avec runbooks, wrappers cmd/menu/sanity, script admin reel, dashboard de visualisation. |
| **Preuves repo** | `docs/status/desk_pro_stack_canonique.md`, `docs/desk_pro_multi_machine_map.md`, `docs/desk_pro_multi_machine_quick_reference.md`, `docs/desk_pro_release_ops_runbook.md`, `docs/ot/project_cards/PROJECT_CARD_DESKPRO_01.md`, `docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md`, `scripts/admin_trading/desk_pro_cmd.sh` |
| **Gap principal** | Consolidation produit : survivant unique non fige, frontiere desk_pro vs desk_* encore en cours de clarification documentaire. |
| **NEXT_GO ou condition** | `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` (reprise existante). |

---

## Candidat 02 -- Bot Vision

| Champ | Valeur |
| --- | --- |
| **Nom** | Bot Vision |
| **Type** | Produit (pipeline vision multi-modules) |
| **Modules principaux** | `vision_bot` (capture/inbox-outbox), `bot_vision_step2` (analyse Vision/Telegram + artefacts Desk Pro), `bot_vision` (legacy) |
| **Role final prevu** | Pipeline de capture screenshot -> analyse Vision -> artefacts Desk Pro/Telegram. |
| **Usage actuel prouve** | Chaine operative transitoire active : `vision_bot` + `bot_vision_step2`. Branches admin-trading documentent le pipeline. |
| **Preuves repo** | `docs/status/bot_vision_canonique.md`, `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`, `docs/ot/project_cards/PROJECT_CARD_BOT_VISION_INGESTION_01.md`, branches admin-trading `*BOT_VISION*`, `*HEADLESS*` |
| **Gap principal** | Pas de survivant unique fige. Transition `bot_vision_step2` encore en cours de stabilisation structurelle. |
| **NEXT_GO ou condition** | `VISION_FAMILY_SURVIVOR_DECISION` si un survivant unique doit etre materialise, ou poursuite de la consolidation via child existant. |

---

## Candidat 03 -- Trading Dual Stack V1 / XAUUSD

| Champ | Valeur |
| --- | --- |
| **Nom** | Trading Dual Stack V1 / XAUUSD |
| **Type** | Produit (framework trading) |
| **Modules principaux** | `modules/trading_lab_v1/`, `modules/trading_realtime_v1/`, `modules/execution_engine/`, `modules/position_engine/`, `modules/portfolio_engine/`, `modules/strategy_engine/` |
| **Role final prevu** | Framework trading unifie LAB/REALTIME, perimetre XAUUSD borne, avec observation puis validation avant autonomie. |
| **Usage actuel prouve** | Schemas et config V1 etablis. Chaine LAB operationnelle, comparateur operationnel. Chaine REALTIME minimale posee. V1 close de maniere repo-sourcee. |
| **Preuves repo** | `docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md` |
| **Gap principal** | V1 close mais bornee : sans broker connecte, sans passage d'ordre reel, sans auto-trading. |
| **NEXT_GO ou condition** | `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` (uniquement si besoin d'extension reelle identifie). |

---

## Candidat 04 -- TradingView / Telegram Alert Pipeline

| Champ | Valeur |
| --- | --- |
| **Nom** | TradingView / Telegram Alert Pipeline |
| **Type** | Produit (pipeline d'alertes et d'observation) |
| **Modules principaux** | `modules/tradingview_observer/`, `modules/tradingview_observer_openclaw/`, `modules/webhook/`, `webhook_server.py` |
| **Role final prevu** | Pipeline de reception d'alertes TradingView -> webhook -> observation -> notification Telegram -> journalisation. |
| **Usage actuel prouve** | Parent observer merged (PR #200). Alert webhook en continuite active (PR #203). Templates et smoke documentes. Bridge packet dry-run fonctionnel. |
| **Preuves repo** | `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` (bloc CURSOR_AI), `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/90_CLOSEOUT.md`, `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_APPLICATION_ACTIVE_01/` |
| **Gap principal** | Alert webhook non ferme. Export reel et integration Telegram a consolider. |
| **NEXT_GO ou condition** | Poursuite du GO alert webhook actif, puis closeout de la continuite. |

---

## Candidat 05 -- OpenClaw Runtime

| Champ | Valeur |
| --- | --- |
| **Nom** | OpenClaw Runtime |
| **Type** | Produit (runtime d'orchestration IA) |
| **Modules principaux** | `modules/gateway_openclaw/`, `modules/configure_openclaw/`, `modules/install_module_openclaw/`, `modules/doctor_openclaw/`, `modules/evidence_openclaw/`, `modules/model_provider_openclaw/`, `modules/menu_openclaw/`, `modules/tradingview_observer_openclaw/`, `modules/openclaw_config_modulaire/` |
| **Role final prevu** | Orchestration IA openclaw comme couche runtime controlee au-dessus des surfaces trading. |
| **Usage actuel prouve** | Modules installables, gateway, configuration. Cartographie documentaire (77 sources). TMUX supervision runtime (child doc-only merge). Orchestration parent ouvert. |
| **Preuves repo** | `docs/product_targets/OPENCLAW_TARGET_CANON.md`, `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01/` |
| **Gap principal** | Orchestration runtime encore en construction. Gateway supervision TMUX en cours, agents non deployes. Synthese runtime unifiee absente. |
| **NEXT_GO ou condition** | `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` (en cours) puis agents runtime. |

---

## Candidat 06 -- LocalCMS (Consumer UI)

| Champ | Valeur |
| --- | --- |
| **Nom** | LocalCMS |
| **Type** | Produit (UI consommatrice externe) |
| **Modules principaux** | `localcms/` (projet consommateur separe), `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/` |
| **Role final prevu** | Consumer UI de opt-trading : lecture /shared, exploration modules, futur cockpit utilisateur. |
| **Usage actuel prouve** | Cadrage et plan documentes. GO UI LocalCMS consumer parent ouvert. Forms integration en cadrage. |
| **Preuves repo** | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/`, `docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/`, `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md` |
| **Gap principal** | Projet consommateur externe, pas de runtime integre dans le repo. Usage reel encore a prouver. |
| **NEXT_GO ou condition** | `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` puis preuve d'usage reel. |

---

## Candidat 07 -- derivates_collector

| Champ | Valeur |
| --- | --- |
| **Nom** | derivatives_collector |
| **Type** | Module produit (collecteur canonique) |
| **Modules principaux** | `modules/derivatives_collector/` |
| **Role final prevu** | Collecteur canonique de donnees marches derives, compatible famille collector. |
| **Usage actuel prouve** | Module operationnel, multi-versions (V3->V13). En cours de convergence doctrinale avec la famille collector. Migration runtime non forcee. |
| **Preuves repo** | `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`, `docs/COLLECTORS_MIGRATION_MAP_01.md` |
| **Gap principal** | Convergence doctrinale en cours (phases 0-5). Artifacts, vocabulaire, config et surface operateur a aligner. |
| **NEXT_GO ou condition** | `GO_COLLECTORS_BASELINE_INVENTORY_01` (phase 0 de la migration map). |

---

## Candidat 08 -- derivates_analyzer

| Champ | Valeur |
| --- | --- |
| **Nom** | derivatives_analyzer |
| **Type** | Module produit (analyse derivee du collector) |
| **Modules principaux** | `modules/derivatives_analyzer/` |
| **Role final prevu** | Analyse structuree et export des donnees collectees par derivatives_collector. |
| **Usage actuel prouve** | Module present, connecte au collector. Mentionne dans PROJECT_SNAPSHOT et ui_indexation. Preuve d'usage moins documentee que le collector lui-meme. |
| **Preuves repo** | `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md`, `docs/ui_indexation/02_ui_registry_wrappers.md` |
| **Gap principal** | Documentation d'usage et de sortie moins explicite que celle du collector. |
| **NEXT_GO ou condition** | Documenter le role exact et les sorties prouvees avant toute promotion. |

---

## Candidat 09 -- probability_engine

| Champ | Valeur |
| --- | --- |
| **Nom** | probability_engine |
| **Type** | Module (moteur d'analyse) |
| **Modules principaux** | `modules/probability_engine/` |
| **Role final prevu** | Synthese probabiliste pour le trading. |
| **Usage actuel prouve** | Module present dans le repo. Mentionne dans PROJECT_SNAPSHOT. Wrapper cmd existant. Preuve d'usage operateur moins documentee. |
| **Preuves repo** | `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md`, `docs/ui_indexation/02_ui_registry_wrappers.md` |
| **Gap principal** | Manque de documentation de closeout ou de preuve d'usage produit explicite. |
| **NEXT_GO ou condition** | Fournir une preuve d'usage (closeout, runbook, smoke) avant de proposer une entree Atlas. |

---

## Candidat 10 -- risk_engine

| Champ | Valeur |
| --- | --- |
| **Nom** | risk_engine |
| **Type** | Module (calcul risque) |
| **Modules principaux** | `modules/risk_engine/` |
| **Role final prevu** | Calcul de risque extrait du webhook pour les prises de decision trading. |
| **Usage actuel prouve** | Module present. Mentionne dans PROJECT_SNAPSHOT. |
| **Preuves repo** | `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md`, `docs/ui_indexation/02_ui_registry_wrappers.md` |
| **Gap principal** | Preuve d'usage produit explicite manquante. |
| **NEXT_GO ou condition** | Fournir une preuve d'usage avant toute promotion. |

---

## Candidat 11 -- Deepseek Student

| Champ | Valeur |
| --- | --- |
| **Nom** | Deepseek Student |
| **Type** | Produit (famille LLM cote student) |
| **Modules principaux** | `modules/deepseek_hub/` (facade unifiee), `modules/deepseek_response/` (compat), `modules/deepseek_thinking/` (compat), `modules/deepseek_student/` (transition), `scripts/student/` |
| **Role final prevu** | Interface LLM operationnelle pour la surface student. |
| **Usage actuel prouve** | Runbook operateur existant. deepseek_hub confirme comme facade module la plus avancee. Runtime reel dans scripts/student/. |
| **Preuves repo** | `docs/status/deepseek_student_canonique.md`, `docs/student_deepseek_runbook.md`, `docs/student_deepseek_quick_reference.md`, `docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md` |
| **Gap principal** | Survivant canonique final non fige. Transition deepseek_student incomplete. |
| **NEXT_GO ou condition** | `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` ou child dedie a la bascule scripts/student/ -> modules/. |

---

## Candidat 12 -- Collectors spot (CoinGecko, Binance)

| Champ | Valeur |
| --- | --- |
| **Nom** | Collectors spot (CoinGecko, Binance) |
| **Type** | Modules produit (collecteurs spot valides) |
| **Modules principaux** | `modules/collector_coingecko/`, `modules/collector_binance_spot/` |
| **Role final prevu** | Collecteurs spot normalises sur la base commune `collectors_core`. |
| **Usage actuel prouve** | Modules valides sur `collectors_core`. Doctrine famille appliquee. |
| **Preuves repo** | `docs/COLLECTORS_FAMILY_DOCTRINE_01.md` |
| **Gap principal** | Font partie d'une famille en convergence. Leur statut individuel est clair mais subordonne a la doctrine famille. |
| **NEXT_GO ou condition** | Suivre la migration map collector. |

---

## Candidat 13 -- Simex Bitget Bridge

| Champ | Valeur |
| --- | --- |
| **Nom** | Simex Bitget Bridge |
| **Type** | Module (bridge echange) |
| **Modules principaux** | `modules/simex_bitget_bridge/` |
| **Role final prevu** | Bridge de simulation/backtest entre opt-trading et l'API Bitget. |
| **Usage actuel prouve** | Presets, contrat d'unites, documentation SIMEX. |
| **Preuves repo** | `docs/simex/SIMEX_PRESETS.md`, `docs/simex/SIMEX_UNITS_CONTRACT.md` |
| **Gap principal** | Documentation utile mais preuve d'usage operateur systematique a confirmer. |
| **NEXT_GO ou condition** | Fournir une preuve d'usage (closeout, smoke) avant promotion. |

---

## Candidat 14 -- Git Fleet Guard

| Champ | Valeur |
| --- | --- |
| **Nom** | Git Fleet Guard |
| **Type** | Module (outillage Git) |
| **Modules principaux** | `modules/git_fleet_guard/` |
| **Role final prevu** | Garde-fou Git multi-machine, anti-conflit et proprete de branche. |
| **Usage actuel prouve** | Module documente avec runbook et module overview. |
| **Preuves repo** | `docs/git_fleet_guard_runbook.md`, `docs/git_fleet_guard_module_overview.md` |
| **Gap principal** | Outillage de support, pas un produit utilisateur final. |
| **NEXT_GO ou condition** | Pas de promotion en produit Atlas. Rester comme outillage documente. |

---

## Candidat 15 -- validated_prompt_factory

| Champ | Valeur |
| --- | --- |
| **Nom** | validated_prompt_factory |
| **Type** | Module (outil operateur) |
| **Modules principaux** | `modules/validated_prompt_factory/` |
| **Role final prevu** | Generateur de prompts structures pour le travail IDE/IA. |
| **Usage actuel prouve** | Module present. Mentionne dans OT_OPS_01_AUDIT comme PARTIEL (manque Registry + Wrapper). |
| **Preuves repo** | `docs/ot/trae/OT_OPS_01_AUDIT.md`, `docs/architecture/REPO_SURFACES_MAP.md` |
| **Gap principal** | Integration incomplete : registry et wrapper manquants. |
| **NEXT_GO ou condition** | Completer registry + wrapper avant de considerer une entree Atlas. |

---

## Candidat 16 -- module_contextuals_shell

| Champ | Valeur |
| --- | --- |
| **Nom** | module_contextuals_shell |
| **Type** | Module (support technique) |
| **Modules principaux** | `modules/module_contextuals_shell/` |
| **Role final prevu** | Coquille technique pour contextualiser des appels modules. |
| **Usage actuel prouve** | Module present mais usage produit non documente. |
| **Preuves repo** | Presence dans `modules/` uniquement. |
| **Gap principal** | Aucune preuve d'usage produit. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. Rester comme module technique. |

---

## Candidat 17 -- Ops wrappers / menus / registries

| Champ | Valeur |
| --- | --- |
| **Nom** | Ops wrappers / menus / registries |
| **Type** | Modules de support (wrappers generiques) |
| **Modules principaux** | `modules/ops_wrappers/`, `modules/ops_menu_hub/`, `modules/ops_super_menu/`, `modules/wrappers_registry_reader/`, `modules/modules_registry_reader/`, `modules/registry_meta_reader/`, `modules/registry_router/`, `modules/machines_registry_reader/` |
| **Role final prevu** | Infrastructure de navigation et d'enregistrement des modules. |
| **Usage actuel prouve** | Modules presents, utilises comme support par d'autres modules. |
| **Preuves repo** | Presence dans `modules/`. |
| **Gap principal** | Ces modules sont des wrappers generiques, pas des produits utilisateur finaux. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. Ce sont des outils internes, pas des produits de l'Atlas. |

---

## Candidat 18 -- Surfaces historiques

| Champ | Valeur |
| --- | --- |
| **Nom** | Surfaces historiques diverses |
| **Type** | Historique |
| **Modules principaux** | `modules/reseau_ssh*`, `modules/perm_fix_student/`, `modules/desk_pro/` (coquille), `scripts/desk_pro_*.sh` (geles), `_archive/` |
| **Role final prevu** | Aucun role produit actif. |
| **Usage actuel prouve** | Certaines surfaces sont explicitement gelees ou archivees. |
| **Preuves repo** | `docs/ot/trae/OT_OPS_05B_DESK_PRO_FREEZE_NOTE.md`, `_archive/` |
| **Gap principal** | Aucun. Ces surfaces ne doivent pas etre promues. |
| **NEXT_GO ou condition** | ARCHIVE_ONLY. Rester hors de l'Atlas. |
