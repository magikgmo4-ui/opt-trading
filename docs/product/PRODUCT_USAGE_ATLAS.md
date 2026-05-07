---
doc_id: OPT_TRADING_PRODUCT_USAGE_ATLAS
doc_type: product_usage_atlas
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/product/guides/README.md
---

# Product Usage Atlas

## Regle de lecture

Chaque entree ci-dessous dit ce que le produit doit devenir, ce qu'il est vraiment aujourd'hui, et comment le lire sans surevaluer son etat.

## CLICKUP_COCKPIT

- `product_name`: ClickUp Cockpit
- `parent_branch`: `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01`
- `reason_to_exist`: piloter les GO, branches, machines, PR, validations et points de reprise dans une UI humaine.
- `final_usage_target`: cockpit operateur transverse pour suivre les lots actifs sans perdre la preuve repo.
- `current_state`: `USABLE_LIMITED`
- `usable_now`: `limited`
- `usage_mode`: usage humain via l'UI ClickUp, avec le repo comme preuve de fond.
- `user_guide`: `docs/product/guides/CLICKUP_COCKPIT.md`
- `canonical_sources`:
  - `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/90_CLOSEOUT.md`
  - `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01/90_CLOSEOUT.md`
  - `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/90_CLOSEOUT.md`
- `remaining_gaps`: statuses personnalises, dashboards et template restent limites par le plan gratuit.
- `next_go`: ouvrir un child dedie seulement si upgrade plan ou besoin reel sur ces limites.
- `do_not_use_notes`: ne jamais traiter ClickUp comme source canonique.

## REPO_KG

- `product_name`: Repo KG
- `parent_branch`: `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`
- `reason_to_exist`: projeter le repo en graphe lisible pour naviguer vite entre GO, docs, modules, branches, gaps et reprises.
- `final_usage_target`: vue repo-first multi-surfaces avec lecture produit, usage reel et overlays de priorite.
- `current_state`: `USABLE_NOW`
- `usable_now`: `yes`
- `usage_mode`: projection read-only reconstruisible depuis le repo et exploitable tout de suite.
- `user_guide`: `docs/product/guides/REPO_KG.md`
- `canonical_sources`:
  - `docs/chantiers/GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01/10_EXECUTION_SUMMARY.md`
  - `docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01/90_CLOSEOUT.md`
  - `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/09_graph_views_v1.md`
- `remaining_gaps`: la vue produit / usage reel au-dessus du bundle reste a renforcer et a maintenir.
- `next_go`: `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01`
- `do_not_use_notes`: ne pas traiter `graph_bundle.json` comme source souveraine ; c'est une projection.

## AIRTABLE_ORCHESTRATION_LAYER

- `product_name`: Airtable Orchestration Layer
- `parent_branch`: `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01`
- `reason_to_exist`: fournir une couche legere de journal, review humaine, signaux et exports sans alourdir le coeur repo.
- `final_usage_target`: produit borne avec base Airtable, bridge optionnel, exports JSON/CSV et role humain clair.
- `current_state`: `DOC_ONLY_READY / GO_LIMITED`
- `usable_now`: `no`
- `usage_mode`: lecture des plans et du finish plan uniquement ; pas de guide live final a ce stade.
- `user_guide`: `none_yet`
- `canonical_sources`:
  - `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md`
  - `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md`
  - `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/02_INTEGRATION_ARCHITECTURE.md`
- `remaining_gaps`: bridge `modules/airtable_bridge/`, tables produit finales, exports controles, preuve d'usage borne.
- `next_go`: `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01`
- `do_not_use_notes`: ne pas presenter Airtable comme source canonique, moteur trading live ou DB historique.

## BOTPRESS_ADAPTER

- `product_name`: Botpress Adapter
- `parent_branch`: `go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01`
- `reason_to_exist`: router des intentions conversationnelles de facon controlee entre Telegram, Botpress, OpenClaw et les surfaces trading.
- `final_usage_target`: operateur conversationnel borne avec safety gate, webhook reel et journalisation structuree.
- `current_state`: `SIMULATED_PASS`
- `usable_now`: `test_only`
- `usage_mode`: simulation et smoke seulement ; la safety gate doit rester active.
- `user_guide`: `docs/product/guides/BOTPRESS_ADAPTER_SIMULATED.md`
- `canonical_sources`:
  - `docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/README.md`
  - `docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01/90_CLOSEOUT.md`
  - `docs/chantiers/GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01/90_CLOSEOUT.md`
- `remaining_gaps`: Telegram reel, webhook reel, credentials et smoke production controle.
- `next_go`: `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01`
- `do_not_use_notes`: ne jamais presenter la simulation comme usage live ; aucun trade reel automatique.

## OPENCLAW_DOCS_LIBRARY

- `product_name`: OpenClaw Docs Library
- `parent_branch`: `go/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01`
- `reason_to_exist`: cartographier les surfaces documentaires OpenClaw pour servir de librairie de recherche repo-first.
- `final_usage_target`: base documentaire claire pour les futurs GOs OpenClaw, puis synthese unifiee.
- `current_state`: `DOC_ONLY_READY`
- `usable_now`: `read_only`
- `usage_mode`: lecture, orientation et reperage des surfaces documentaires.
- `user_guide`: `docs/product/guides/OPENCLAW_DOCS_LIBRARY.md`
- `canonical_sources`:
  - `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/00_CADRAGE_PARENT.md`
  - `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/01_SOURCE_CARTOGRAPHY.md`
  - `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/90_CLOSEOUT.md`
- `remaining_gaps`: raffiner la cartographie, faire le deep dive des composants et produire une synthese finale unifiee.
- `next_go`: `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01`
- `do_not_use_notes`: ce n'est pas un wiki final ni une surface runtime.

## BTC_COINM_ACCUMULATION_ENGINE

- `product_name`: BTC COIN-M Accumulation Engine
- `parent_branch`: `go/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01`
- `reason_to_exist`: cadrer un moteur mathematique d'accumulation BTC avec logique COIN-M, sans ouvrir prematurement du runtime ou du backtest non fiable.
- `final_usage_target`: moteur valide avec formules figees, bornes, backtest, worker et garde-fous reellement prouves.
- `current_state`: `NOT_USABLE_YET / DO_NOT_USE_LIVE`
- `usable_now`: `no`
- `usage_mode`: lecture du cadrage seulement ; aucun usage live, aucun backtest fiable, aucun worker.
- `user_guide`: `none_yet`
- `canonical_sources`:
  - `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md`
  - `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md`
  - `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md`
- `remaining_gaps`: validation utilisateur du parent, formules Bitget, compatibilite, backtest data prep, worker et invariants prouves.
- `next_go`: valider le parent puis ouvrir le child formules dedie avant toute suite runtime.
- `do_not_use_notes`: aucun runtime trading reel, aucun guide live, aucun branchement exchange.
