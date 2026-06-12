---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01_SYNTHESIS
doc_type: synthesis_and_hypothetical_tree
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: synthesis
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/01_REPO_PRODUCT_CANDIDATES.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/01b_REPO_PRODUCT_CANDIDATES_ADDENDUM.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/03_ATLAS_UPDATE_PROPOSAL.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# SYNTHESE & ARBRE HYPOTHETIQUE -- opt-trading

## PARTIE 1 -- RECAPITULATIF DE TOUS LES INVENTAIRES

### Socle initial (Parent Atlas + Usage View child)

| Produit | Bucket usage | Statut produit | NEXT_GO |
| --- | --- | --- | --- |
| ClickUp Cockpit | `USABLE_LIMITED` | `USABLE_LIMITED` | Besoin reel ou upgrade plan seulement |
| Repo KG | `USABLE_NOW` | `USABLE_NOW` | `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01` |
| Airtable Orchestration Layer | `DOC_ONLY` | `DOC_ONLY_READY / GO_LIMITED` | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| Botpress Adapter | `SIMULATED_ONLY` | `SIMULATED_PASS` | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |
| OpenClaw Docs Library | `DOC_ONLY` | `DOC_ONLY_READY` | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` |
| BTC COIN-M Accumulation Engine | `FORBIDDEN_LIVE` | `NOT_USABLE_YET / DO_NOT_USE_LIVE` | Valider parent puis child formules dedie |

**Total socle : 6 produits**

### Inventaire elargi (Repo Inventory child)

| Decision | Nombre | Surfaces |
| --- | --- | --- |
| ADD_TO_ATLAS | 7 | Desk Pro, Bot Vision, Trading Dual Stack V1, TradingView/Telegram Alert Pipeline, OpenClaw Runtime, LocalCMS, derivatives_collector |
| KEEP_CANDIDATE | 16 | derivatives_analyzer, probability_engine, risk_engine, Deepseek Student, Collectors spot, Simex Bitget Bridge, validated_prompt_factory, market_scanner, decision_engine, execution_engine, journal_engine, liquidation_analyzer, opportunity_ranker, perf_engine, marketdata + 1 autre |
| DO_NOT_PROMOTE | 27 | Git Fleet Guard, module_contextuals_shell, Ops wrappers, surfaces historiques, memory_bricks, workflow_ai, deploy_module_multi_machine, webhook_server.py, bitget_bridge.py, hf_free_platform, mimo_open_observer, workflow_post_change_v2, collectors_core, + 14 modules de support |
| ARCHIVE_ONLY | ~12 | bot_vision legacy, reseau_ssh legacy, desk_pro scripts geles, _archive/, trae_pack_texts legacy, bitget_bridge shim |
| UNKNOWN_NEEDS_RESCAN | 1 | kil_v1 |
| A AUDITER | ~10 | kil_v1, hf_free_platform, mimo_open_observer, marketdata, strategy_engine, webhook_server.py, e2e_telegram_smoke.py, smoke_adapter.py, smoke.sh, smoke_tv_engine.py |

**Total elargi : ~51 surfaces identifiees, 38 modules/88 modules classifies par role**

---

## PARTIE 2 -- DIMENSIONS DE CLASSIFICATION AJOUTEES

### 2.1 APPARTENANCE (famille / sous-projet)

| Famille | Membres | Type famille |
| --- | --- | --- |
| APPS_EXTERNES | ClickUp, Airtable, Botpress, LocalCMS | Apps connectees au repo |
| DESK_PRO | desk_pro_runner, desk_pro_orchestrator, desk_pro_dashboard, desk_common, desk_state, desk_analyze, desk_capture_inputs, desk_retention, desk_snapshot_ingest, desk_pro (coquille) | Stack operationnelle |
| BOT_VISION | vision_bot (survivant), bot_vision_step2 (survivant), bot_vision (legacy) | Pipeline vision |
| TRADING_DUAL_STACK | trading_lab_v1, trading_realtime_v1, execution_engine, position_engine, portfolio_engine, strategy_engine | Framework trading unifie |
| TRADINGVIEW_PIPELINE | tradingview_observer, tradingview_observer_openclaw, webhook (module), webhook_server.py (racine), tradingview/smartmoney*.pine | Pipeline alertes |
| OPENCLAW | gateway_openclaw, configure_openclaw, install_module_openclaw, doctor_openclaw, evidence_openclaw, model_provider_openclaw, menu_openclaw, openclaw_config_modulaire, tradingview_observer_openclaw | Orchestration IA |
| COLLECTORS | derivatives_collector, collector_coingecko, collector_binance_spot, derivatives_analyzer, collectors_core (package), marketdata | Collecte de donnees |
| ENGINES_ANALYSIS | probability_engine, risk_engine, decision_engine, market_scanner, opportunity_ranker, liquidation_analyzer, perf_engine, perf (module), perf_app.py | Moteurs d'analyse |
| JOURNAL | journal_engine | Journalisation |
| DEEPSEEK | deepseek_hub, deepseek_response, deepseek_thinking, deepseek_student, scripts/student/ | LLM student |
| BITGET | simex_bitget_bridge, bitget_bridge.py (shim) | Bridge echange |
| REPO_KG | producer_repo_kg_v1.py, graph_bundle.json | Knowledge graph |
| COUCHE_PRODUIT | docs/product/* (Atlas, Matrix, Gaps, Protocol, Guides, Graph) | Lecture utilisateur |
| GOUVERNANCE | docs/governance/*, docs/index/*, workflow_ai/ | Regles et processus |
| OPS_WRAPPERS | ops_wrappers, ops_menu_hub, ops_super_menu, wrappers_registry_reader, modules_registry_reader, registry_meta_reader, registry_router, machines_registry_reader | Infrastructure operateur |
| DEV_INFRA | git_fleet_guard, repo_hygiene, repo_local_artifacts, repo_ownership_guard, dev_validation_hub, trae_module_validator, module_contextuals_shell, naming_normalizer, install_module, install_module_openclaw, deploy_module_multi_machine, validated_prompt_factory, audit | Outillage dev |
| SHARED_INFRA | shared, shared_files_sftp, shared_sshfs_permanent, winscp_transfer, env, health, auth, router, scripts (module), engines (module) | Infrastructure partagee |
| BTC_COINM | trading_parent_btc_coinm_accumulation_engine | Moteur accumulation |
| MEMORY | memory_bricks | Compaction derivee |
| HERITAGE | reseau_ssh*, perm_fix_student, desk_pro (coquille), bot_vision (legacy), bitget_bridge.py (shim), _archive/*, trae_pack_texts/* | Historique/legacy |
| INCONNU | kil_v1, hf_free_platform, mimo_open_observer | A auditer |

### 2.2 DEPENDANCE (ce dont chaque famille depend)

| Famille | Depend de |
| --- | --- |
| DESK_PRO | BOT_VISION (capture), TRADINGVIEW_PIPELINE (alertes), SHARED_INFRA, COLLECTORS (donnees) |
| BOT_VISION | DESK_PRO (artefacts), SHARED_INFRA, Telegram |
| TRADING_DUAL_STACK | COLLECTORS (donnees), ENGINES_ANALYSIS (calculs), BITGET (broker cible) |
| TRADINGVIEW_PIPELINE | OPENCLAW (observer), DESK_PRO (consommation), Telegram, webhook |
| OPENCLAW | SHARED_INFRA, DEEPSEEK (modeles), GOUVERNANCE |
| COLLECTORS | BITGET (API), SHARED_INFRA, packages/collectors_core |
| ENGINES_ANALYSIS | COLLECTORS (donnees), TRADING_DUAL_STACK (contexte), JOURNAL |
| DEEPSEEK | OPENCLAW, scripts/student/, Ollama |
| BITGET | COLLECTORS, TRADING_DUAL_STACK |
| APPS_EXTERNES | COUCHE_PRODUIT (lecture), GOUVERNANCE (regles) |
| COUCHE_PRODUIT | REPO_KG (bundle), GOUVERNANCE (regles), tous les closeouts |
| REPO_KG | GOUVERNANCE (GO_INDEX, BRANCH_STATE), tout le repo |
| BTC_COINM | BITGET (formules), ENGINES_ANALYSIS, TRADING_DUAL_STACK (backtest) |

### 2.3 MASTER TARGET PROJECT vs TARGET ADD-ON

| Niveau | Surfaces | Description |
| --- | --- | --- |
| **MASTER** (coeur souverain) | REPO_KG, COUCHE_PRODUIT, GOUVERNANCE, TRADING_DUAL_STACK, COLLECTORS, ENGINES_ANALYSIS, DESK_PRO | Le coeur du systeme : repo, projection, regles, trading, collecte, analyse, desk |
| **TARGET_ADD_ON** (extension planifiee) | APPS_EXTERNES (ClickUp, Airtable, Botpress, LocalCMS), OPENCLAW, BOT_VISION, TRADINGVIEW_PIPELINE, DEEPSEEK, BITGET, BTC_COINM | Extensions qui enrichissent le coeur sans le remplacer |

### 2.4 CANDIDATS A CONSOLIDER (modules multi-versions, doublons, ou eclates)

| Candidat | Composants eclates | Recommandation |
| --- | --- | --- |
| STRATEGIE | `modules/strategy_engine/` (module isole), `modules/decision_engine/` (decisions), `modules/execution_engine/` (execution), `modules/position_engine/` (positions), `modules/portfolio_engine/` (portefeuille) | Consolider en une famille STRATEGY avec sous-modules clairs. Aujourd'hui eclate et peu documente. |
| UI / DASHBOARD | `modules/desk_pro_dashboard/` (desk), `modules/ui_registry_msi/` (MSI), `modules/market_scanner/` (scanning), `LocalCMS` (externe) | Definir une cible UI unifiee. Aujourd'hui morcele entre desk, MSI, scanner et LocalCMS. |
| PERF | `modules/perf_engine/` (prouve live), `modules/perf/` (analyse), `perf/perf_app.py` (racine), `adapters/webhook_to_perf.py` (pont) | Unifier sous `perf_engine` comme produit, le reste comme support. |
| DEEPSEEK | `modules/deepseek_hub/` (facade), `modules/deepseek_student/` (transition), `modules/deepseek_response/`, `modules/deepseek_thinking/` (compat), `scripts/student/` (runtime) | Figer `deepseek_hub` comme survivant canonique, migrer scripts/student/ vers modules/. |
| BOT_VISION | `modules/vision_bot/` (capture), `modules/bot_vision_step2/` (analyse), `modules/bot_vision/` (legacy) | Figer `vision_bot` + `bot_vision_step2` comme produit, archiver `bot_vision`. |
| COLLECTORS | `modules/derivatives_collector/` (canonique), `modules/collector_coingecko/` (spot), `modules/collector_binance_spot/` (spot), `packages/collectors_core/` (base), `modules/marketdata/` (flou) | Suivre la migration map (phases 0-5). Clarifier le role de marketdata. |
| OPENCLAW | 9 modules OpenClaw + 2 observers + docs | Cartographie terminee (77 sources). Prochaine etape : synthese runtime unifiee. |
| SCRIPTS_LEGACY | `scripts/desk_pro_*.sh` (geles), `scripts/reseau_*`, `scripts/ui_debug/`, `scripts/db_layer/`, `scripts/desk_bridge/` | Certains sont geles (OT_OPS_05B), d'autres sont des supports operationnels. A auditer pour nettoyage. |

---

## PARTIE 3 -- ARBRE HYPOTHETIQUE

> **NOTE CANONIQUE :** Cet arbre est une hypothese structurante et une aide de priorisation. Il ne promeut aucun produit, ne remplace pas `PRODUCT_USAGE_MATRIX.md`, et ne constitue pas une source canonique. L'ordre de verite reste : (1) `PRODUCT_USAGE_MATRIX.md`, (2) `PRODUCT_USAGE_ATLAS.md`, (3) `FINAL_TARGET_GAPS.md`, (4) `03_ATLAS_UPDATE_PROPOSAL.md`, (5) ce fichier.

### 3.1 MASTER PLAN PROJECT (architecture logique souhaitee)

```text
opt-trading (repo canonique)
│
├── [COEUR SOUVERAIN] ─────────────────────────────────────────────
│   │
│   ├── REPO_KG (USABLE_NOW)
│   │   ├── producer_repo_kg_v1.py
│   │   └── graph_bundle.json
│   │       -> NEXT: enrichir avec inventaire elargi
│   │
│   ├── COUCHE_PRODUIT (USABLE_NOW, doc-only)
│   │   ├── PRODUCT_USAGE_MATRIX.md
│   │   ├── PRODUCT_USAGE_ATLAS.md
│   │   ├── FINAL_TARGET_GAPS.md
│   │   ├── UPDATE_PROTOCOL.md
│   │   ├── PRODUCT_USAGE_GRAPH.mmd
│   │   └── guides/
│   │       -> NEXT: appliquer ADD_TO_ATLAS (7 entrees) + user guides
│   │
│   ├── GOUVERNANCE (USABLE_NOW, doc-only)
│   │   ├── GO_INDEX.md, BRANCH_STATE.md, REPRISE.md
│   │   ├── MATRICE_DOC_OPS_MASTER_MATRIX_01.md
│   │   ├── MATRICE_GOUVERNANTE_V2.md
│   │   ├── REPO_ROLE.md, REPO_ROOT_POLICY.md
│   │   ├── workflow_ai/WORKFLOW.md
│   │   └── HUMAN_CONTINUITY_*.md
│   │
│   ├── COLLECTORS (USABLE_LIMITED)
│   │   ├── derivatives_collector (canonique)
│   │   ├── collector_coingecko (spot)
│   │   ├── collector_binance_spot (spot)
│   │   ├── derivatives_analyzer (KEEP_CANDIDATE)
│   │   ├── marketdata (A AUDITER)
│   │   └── collectors_core (package)
│   │       -> GAP: convergence doctrinale (phases 0-5)
│   │       -> NEXT: GO_COLLECTORS_BASELINE_INVENTORY_01
│   │
│   ├── ENGINES_ANALYSIS (DOC_ONLY / KEEP_CANDIDATE)
│   │   ├── probability_engine
│   │   ├── risk_engine
│   │   ├── decision_engine
│   │   ├── market_scanner
│   │   ├── opportunity_ranker
│   │   ├── liquidation_analyzer
│   │   ├── perf_engine (USABLE_LIMITED, prouve live)
│   │   └── journal_engine
│   │       -> GAP: pas de closeout produit unifie
│   │       -> CANDIDAT A CONSOLIDER: famille STRATEGY
│   │
│   └── DESK_PRO (USABLE_LIMITED)
│       ├── desk_pro_runner (facade)
│       ├── desk_pro_orchestrator (pipeline)
│       ├── desk_pro_dashboard (UI)
│       ├── desk_common (support)
│       ├── desk_analyze, desk_capture_inputs, desk_state
│       ├── desk_retention, desk_snapshot_ingest
│       └── desk_pro (coquille gelee, ARCHIVE)
│           -> GAP: survivant unique non fige
│           -> NEXT: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
│
├── [EXTENSIONS PLANIFIEES] ───────────────────────────────────────
│   │
│   ├── TRADING_DUAL_STACK (DOC_ONLY)
│   │   ├── trading_lab_v1 (operationnel)
│   │   ├── trading_realtime_v1 (minimal)
│   │   ├── execution_engine
│   │   ├── position_engine
│   │   ├── portfolio_engine
│   │   └── strategy_engine
│   │       -> GAP: sans broker reel, sans ordre reel
│   │       -> NEXT: GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01
│   │
│   ├── BOT_VISION (USABLE_LIMITED)
│   │   ├── vision_bot (capture/inbox-outbox, survivant)
│   │   ├── bot_vision_step2 (analyse/Telegram, survivant)
│   │   └── bot_vision (legacy, ARCHIVE)
│   │       -> GAP: survivant unique non fige
│   │       -> NEXT: VISION_FAMILY_SURVIVOR_DECISION
│   │
│   ├── TRADINGVIEW_PIPELINE (USABLE_LIMITED)
│   │   ├── tradingview_observer (merged)
│   │   ├── tradingview_observer_openclaw
│   │   ├── webhook (module)
│   │   ├── webhook_server.py (racine, A AUDITER)
│   │   └── smartmoney_webhook_server_compat.pine
│   │       -> GAP: alert webhook non ferme
│   │       -> NEXT: poursuite GO alert webhook actif
│   │
│   ├── OPENCLAW_RUNTIME (USABLE_LIMITED)
│   │   ├── gateway_openclaw
│   │   ├── configure_openclaw
│   │   ├── 7 autres modules
│   │   └── docs library (77 sources)
│   │       -> GAP: orchestration runtime en construction
│   │       -> NEXT: TMUX supervision -> agents -> synthese
│   │
│   ├── DEEPSEEK_STUDENT (KEEP_CANDIDATE)
│   │   ├── deepseek_hub (facade)
│   │   ├── deepseek_student (transition)
│   │   ├── deepseek_response, deepseek_thinking (compat)
│   │   └── scripts/student/ (runtime)
│   │       -> GAP: survivant final non fige
│   │       -> CANDIDAT A CONSOLIDER
│   │
│   ├── BITGET_BRIDGE (KEEP_CANDIDATE)
│   │   ├── simex_bitget_bridge (canonique)
│   │   └── bitget_bridge.py (shim, ARCHIVE)
│   │       -> GAP: preuve d'usage systematique
│   │
│   ├── BTC_COINM (FORBIDDEN_LIVE)
│   │   └── trading_parent_btc_coinm_accumulation_engine
│   │       -> GAP: draft, formules non validees
│   │       -> NEXT: valider parent puis child formules
│   │
│   └── APPS_EXTERNES
│       ├── ClickUp Cockpit (USABLE_LIMITED)
│       ├── Airtable (DOC_ONLY)
│       ├── Botpress (SIMULATED_ONLY)
│       └── LocalCMS (DOC_ONLY)
│           -> GAP: Airtable bridge, Botpress Telegram reel, LocalCMS runtime
│
├── [SUPPORT & INFRA] ─────────────────────────────────────────────
│   │
│   ├── OPS_WRAPPERS (8 modules)
│   ├── DEV_INFRA (~15 modules)
│   ├── SHARED_INFRA (~12 modules)
│   ├── MEMORY_BRICKS (compaction derivee)
│   ├── DEPLOY (deploy_module_multi_machine)
│   └── SCRIPTS_LEGACY (geles ou support)
│
└── [A AUDITER] ───────────────────────────────────────────────────
    ├── kil_v1 (role inconnu)
    ├── hf_free_platform (aucune doc)
    ├── mimo_open_observer (aucune doc)
    ├── strategy_engine (module isole)
    ├── marketdata (role flou)
    ├── webhook_server.py (doublon module webhook?)
    ├── e2e_telegram_smoke.py (perimetre a confirmer)
    ├── smoke_adapter.py (perimetre a confirmer)
    ├── smoke.sh (perimetre a confirmer)
    └── smoke_tv_engine.py (perimetre a confirmer)
```

---

### 3.2 PROJECT PRODUCT FINISH TARGET (cible produit fini par famille)

| Famille | Cible produit fini | Etat actuel | Chemin restant |
| --- | --- | --- | --- |
| DESK_PRO | Stack Desk Pro unifiee avec survivant unique, runbooks complets, dashboard produit | USABLE_LIMITED | Consolidation module families -> survivant unique -> closeout produit |
| BOT_VISION | Pipeline vision avec survivant unique, capture headless, artefacts Desk Pro/Telegram | USABLE_LIMITED | Survivor decision -> stabilisation step2 -> closeout |
| TRADING_DUAL_STACK | Framework LAB/REALTIME avec broker connecte, ordres papier d'abord, puis reel controle | DOC_ONLY | Extension reelle -> broker -> ordres papier -> validation |
| TRADINGVIEW_PIPELINE | Pipeline alertes complet : TradingView -> webhook -> Telegram -> Desk Pro, boucle fermee | USABLE_LIMITED | Closeout alert webhook -> export reel -> integration Telegram |
| COLLECTORS | Famille collector unifiee : doctrine, vocabulaire, artifacts, config, surfaces operateur alignees | USABLE_LIMITED | Phases 0-5 migration map -> convergence -> closeout famille |
| ENGINES_ANALYSIS | Moteurs documentes individuellement, famille STRATEGY consolidee, closeouts par moteur | DOC_ONLY | Documentation par moteur -> consolidation STRATEGY -> closeouts |
| OPENCLAW | Runtime d'orchestration IA complet : gateway, agents, supervision, synthese unifiee | USABLE_LIMITED | TMUX runtime -> agents -> synthese -> closeout runtime |
| DEEPSEEK | deepseek_hub comme survivant unique, migration scripts/student/ vers modules/ | KEEP_CANDIDATE | Survivant final -> migration -> closeout |
| APPS_EXTERNES | ClickUp: OK. Airtable: bridge. Botpress: Telegram reel. LocalCMS: runtime. | DOC_ONLY a USABLE_LIMITED | Airtable bridge, Botpress reel, LocalCMS preuve |
| BTC_COINM | Moteur mathematique valide avec formules, backtest et worker bornes | FORBIDDEN_LIVE | Validation parent -> formules -> compatibilite -> backtest -> worker |

---

### 3.3 APPARTENANCE & COMPATIBILITE (matrice croisee)

| Famille A | Famille B | Lien | Compatibilite |
| --- | --- | --- | --- |
| DESK_PRO | BOT_VISION | BOT_VISION produit les artefacts consommes par DESK_PRO | OK (operationnel) |
| DESK_PRO | TRADINGVIEW_PIPELINE | TRADINGVIEW envoie les alertes vers DESK_PRO | OK (partiellement, alert webhook a fermer) |
| DESK_PRO | COLLECTORS | DESK_PRO lit les donnees collectees | A verifier (dependance indirecte) |
| TRADING_DUAL_STACK | COLLECTORS | DUAL_STACK a besoin des donnees de marche | A etablir (V1 close sans broker) |
| TRADING_DUAL_STACK | ENGINES_ANALYSIS | DUAL_STACK utilise les moteurs pour les decisions | Flou (engines non documentes) |
| TRADING_DUAL_STACK | BITGET | DUAL_STACK cible Bitget comme broker | NON (V1 sans broker) |
| OPENCLAW | TRADINGVIEW_PIPELINE | Observer OpenClaw pour TradingView | OK (module openclaw dedie) |
| OPENCLAW | DEEPSEEK | OpenClaw peut utiliser Deepseek comme modele | A verifier |
| OPENCLAW | BOTPRESS | OpenClaw recoit les requetes routees par Botpress | OK (contrat API etabli, simule) |
| BTC_COINM | BITGET | BTC COIN-M depend des formules Bitget COIN-FUTURES | NON (formules non validees) |
| BTC_COINM | TRADING_DUAL_STACK | COIN-M est un cas specialise de DUAL_STACK | NON (COIN-M est FORBIDDEN_LIVE) |
| APPS_EXTERNES | COUCHE_PRODUIT | Les apps lisent la couche produit pour leurs statuts | OK (doc-only, pas de push auto) |
| REPO_KG | COUCHE_PRODUIT | Le KG projette la couche produit dans le graphe | A enrichir (vue produit a maintenir) |

---

### 3.4 CHANTIERS SANS CONTINUITE ACTUELLE VISIBLE

| Surface / Chantier | Derniere trace visible | Risque |
| --- | --- | --- |
| strategy_engine | Module present, aucun chantier actif | Orphelin. A rattacher a ENGINES_ANALYSIS ou TRADING_DUAL_STACK. |
| kil_v1 | Module present, role inconnu | Orphelin. A auditer en priorite. |
| hf_free_platform | Module present, aucun doc | Orphelin. A auditer. |
| mimo_open_observer | Module present, aucun doc | Orphelin. A auditer. |
| marketdata | Module present, role flou | Orphelin. A rattacher a COLLECTORS. |
| e2e_telegram_smoke.py | Fichier racine, branche Botpress mergee | Proprete racine. A relier a Botpress ou archiver. |
| smoke_adapter.py | Fichier racine, branche Botpress mergee | Proprete racine. A relier a Botpress ou archiver. |
| smoke.sh, smoke_tv_engine.py | Scripts dans scripts/ | A relier a la famille concernee. |
| Decision engine vs execution engine vs strategy | Trois modules eclates sans coordination visible | Candidat a consolider en famille STRATEGY. |
| LocalCMS | Projet externe, GO ouvert mais pas de preuve runtime | Risque de desynchronisation avec le repo. |
| BTC COIN-M formulas child | Ouvert sur branche locale, pas de merge | Bloque tant que le parent n'est pas valide. |

---

### 3.5 SUITE LOGIQUE (ordre de priorite recommande)

```text
PHASE A -- AUDIT & STABILISATION (avant tout nouveau chantier)
─────────────────────────────────────────────────────────────
A1. Auditer les 10 surfaces A AUDITER (kil_v1, hf_free_platform,
    mimo_open_observer, strategy_engine, marketdata, webhook_server.py,
    e2e_telegram_smoke.py, smoke_adapter.py, smoke.sh, smoke_tv_engine.py)
    -> GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01

A2. Figer les candidats a consolider :
    - STRATEGY : decision_engine + execution_engine + strategy_engine +
      position_engine + portfolio_engine
    - UI : desk_pro_dashboard + ui_registry_msi + market_scanner + LocalCMS
    - PERF : perf_engine + perf + perf_app.py + webhook_to_perf.py
    - DEEPSEEK : deepseek_hub + deepseek_student + scripts/student/
    -> GO_OPT_TRADING_CONSOLIDATION_CANDIDATES_01

PHASE B -- FERMETURE DES GAPS PRIORITAIRES
──────────────────────────────────────────
B1. Appliquer ADD_TO_ATLAS dans docs/product/*
    -> GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01

B2. Fermer TradingView alert webhook
    -> Poursuite GO existant

B3. Converger la famille COLLECTORS (phases 0-5)
    -> GO_COLLECTORS_BASELINE_INVENTORY_01

B4. Consolider Desk Pro (survivant unique)
    -> GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01

B5. Figer Bot Vision survivant
    -> VISION_FAMILY_SURVIVOR_DECISION

PHASE C -- EXTENSIONS CONDITIONNELLES
──────────────────────────────────────
C1. Airtable bridge (si GO_LIMITED accepte)
    -> GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01

C2. Botpress Telegram reel (si credentials disponibles)
    -> GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01

C3. Trading Dual Stack extension reelle (si broker et besoin identifies)
    -> GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01

C4. OpenClaw agents runtime (apres TMUX supervision)
    -> GO_OPENCLAW_AGENTS_RUNTIME_01

C5. BTC COIN-M formules (apres validation parent)
    -> GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01

C6. LocalCMS preuve d'usage
    -> GO_LOCALCMS_FORMS_INTEGRATION_DOC_01
```

---

### 3.6 TOTAUX CONSOLIDES (tous inventaires)

| Niveau | Nombre |
| --- | --- |
| Socle initial (Atlas) | 6 produits |
| ADD_TO_ATLAS (nouveaux) | 7 produits |
| KEEP_CANDIDATE | 16 surfaces |
| DO_NOT_PROMOTE | 27 surfaces |
| ARCHIVE_ONLY | ~12 surfaces |
| A AUDITER | 10 surfaces |
| UNKNOWN_NEEDS_RESCAN | 1 surface (kil_v1) |
| **TOTAL SURFACES INVENTORIEES** | **~51** |
| Modules dans `modules/` | 87 entrees |
| Modules classes par role | 77 / 87 (88%) |
| Modules non classes (inconnus) | 10 (kil_v1, hf_free_platform, mimo_open_observer, marketdata, strategy_engine, + 5 fichiers racine/scripts non modules) |
| Familles identifiees | 19 |
| Zones grises documentees | 7 |
| Candidats a consolider | 8 |
| Chantiers sans continuite visible | ~11 |
| NEXT_GO proposes | 15 |

## RISKS

- À qualifier.
