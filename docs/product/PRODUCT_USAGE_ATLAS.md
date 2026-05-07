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
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/01_USAGE_VIEW.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/02_NEXT_GO_BY_PRODUCT.md
---

# Product Usage Atlas

## Regle de lecture

Chaque entree ci-dessous dit ce que le produit doit devenir, ce qu'il est vraiment aujourd'hui, et comment le lire sans surevaluer son etat.

## Usage View - lecture rapide

Cette vue applique une regle simple : quand plusieurs statuts coexistent, la lecture operateur garde le sens le plus prudent.

### Utilisable maintenant

- `Repo KG` : projection repo-first exploitable maintenant ; NEXT_GO = `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01`.

### Utilisable avec limites

- `ClickUp Cockpit` : cockpit operateur utile maintenant, mais encore borne par le plan gratuit ; NEXT_GO = ouvrir un child dedie seulement si besoin reel ou upgrade plan.

### Documente seulement

- `Airtable Orchestration Layer` : produit cadre et documente, pas encore prouve comme usage runtime borne ; NEXT_GO = `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01`.
- `OpenClaw Docs Library` : lecture et cartographie documentaire seulement ; NEXT_GO = `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01`.

### Simule seulement

- `Botpress Adapter` : smokes et simulation seulement ; NEXT_GO = `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01`.

### Interdit live

- `BTC COIN-M Accumulation Engine` : aucun usage live autorise ; NEXT_GO = valider le parent puis ouvrir le child formules dedie.

## CLICKUP_COCKPIT

- `product_name`: ClickUp Cockpit
- `parent_branch`: `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01`
- `reason_to_exist`: piloter les GO, branches, machines, PR, validations et points de reprise dans une UI humaine.
- `final_usage_target`: cockpit operateur transverse pour suivre les lots actifs sans perdre la preuve repo.
- `usage_view`: `USABLE_LIMITED`
- `current_state`: `USABLE_LIMITED`
- `usable_now`: `limited`
- `operator_read`: utilisable maintenant avec limites connues ; ne pas le traiter comme produit fini ni comme source canonique.
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
- `usage_view`: `USABLE_NOW`
- `current_state`: `USABLE_NOW`
- `usable_now`: `yes`
- `operator_read`: utilisable maintenant comme projection read-only reconstruisible ; la preuve finale reste dans le repo.
- `usage_mode`: projection read-only reconstruisible depuis le repo et exploitable tout de suite.
- `user_guide`: `docs/product/guides/REPO_KG.md`
- `canonical_sources`:
  - `docs/chantiers/GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01/10_EXECUTION_SUMMARY.md`
  - `docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01/90_CLOSEOUT.md`
  - `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/09_graph_views_v1.md`
- `remaining_gaps`: etendre la vue usage a plus de produits et modules au-dela du socle initial.
- `next_go`: `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01`
- `do_not_use_notes`: ne pas traiter `graph_bundle.json` comme source souveraine ; c'est une projection.

## AIRTABLE_ORCHESTRATION_LAYER

- `product_name`: Airtable Orchestration Layer
- `parent_branch`: `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01`
- `reason_to_exist`: fournir une couche legere de journal, review humaine, signaux et exports sans alourdir le coeur repo.
- `final_usage_target`: produit borne avec base Airtable, bridge optionnel, exports JSON/CSV et role humain clair.
- `usage_view`: `DOC_ONLY`
- `current_state`: `DOC_ONLY_READY / GO_LIMITED`
- `usable_now`: `no`
- `operator_read`: surface documentee seulement du point de vue usage courant ; ne pas la presenter comme runtime operatoire.
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
- `usage_view`: `SIMULATED_ONLY`
- `current_state`: `SIMULATED_PASS`
- `usable_now`: `test_only`
- `operator_read`: simulation seulement ; ne pas deriver vers une lecture live-ready.
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
- `usage_view`: `DOC_ONLY`
- `current_state`: `DOC_ONLY_READY`
- `usable_now`: `read_only`
- `operator_read`: lecture seulement ; aucune conclusion runtime a tirer depuis cette librairie seule.
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
- `usage_view`: `FORBIDDEN_LIVE`
- `current_state`: `NOT_USABLE_YET / DO_NOT_USE_LIVE`
- `usable_now`: `no`
- `operator_read`: interdit live ; lecture du cadrage seulement jusqu'a validation forte des formules et invariants.
- `usage_mode`: lecture du cadrage seulement ; aucun usage live, aucun backtest fiable, aucun worker.
- `user_guide`: `none_yet`
- `canonical_sources`:
  - `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md`
  - `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md`
  - `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md`
- `remaining_gaps`: validation utilisateur du parent, formules Bitget, compatibilite, backtest data prep, worker et invariants prouves.
- `next_go`: valider le parent puis ouvrir le child formules dedie avant toute suite runtime.
- `do_not_use_notes`: aucun runtime trading reel, aucun guide live, aucun branchement exchange.
