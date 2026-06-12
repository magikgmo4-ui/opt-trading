---
doc_id: OPT_TRADING_PRODUCT_USAGE_ATLAS
doc_type: product_usage_atlas
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/product/guides/README.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/01_USAGE_VIEW.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/02_NEXT_GO_BY_PRODUCT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/03_ATLAS_UPDATE_PROPOSAL.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01/01_DELTA_SCAN.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01/90_CLOSEOUT.md
---

# Product Usage Atlas

## Regle de lecture

Chaque entree ci-dessous dit ce que le produit doit devenir, ce qu'il est vraiment aujourd'hui, et comment le lire sans surevaluer son etat.

## Usage View - lecture rapide

Cette vue applique une regle simple : quand plusieurs statuts coexistent, la lecture operateur garde le sens le plus prudent.

### Utilisable maintenant

- `Repo KG` : projection repo-first exploitable maintenant ; NEXT_GO = maintenance continue via `UPDATE_PROTOCOL.md`, avec rescan Atlas seulement si la couverture ou les guides changent.

### Utilisable avec limites

- `ClickUp Cockpit` : cockpit operateur utile maintenant, mais encore borne par le plan gratuit ; NEXT_GO = ouvrir un child dedie seulement si besoin reel ou upgrade plan.
- `Desk Pro` : stack operationnelle avec runbooks, wrappers et dashboard ; survivant unique non fige ; NEXT_GO = `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01`.
- `Bot Vision` : paire runtime canonique stable (`vision_bot` + `bot_vision_step2`) avec wrappers unifies ; NEXT_GO = `GO_OPT_TRADING_VISION_RUNTIME_STABILIZATION_01`.
- `Deepseek Student` : surface locale DeepSeek/Ollama cote `student`, exploitable via wrappers et runbook ; NEXT_GO = verifier `post_change.sh` avant tout retrait legacy.
- `TradingView / Telegram Alert Pipeline` : pipeline d'alertes actif, alert webhook en continuite ; NEXT_GO = poursuite GO alert webhook actif.
- `OpenClaw Runtime` : modules runtime installables, gateway, TMUX supervision en cours ; NEXT_GO = `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01`.
- `derivatives_collector` : collecteur canonique derives, doctrine famille alignee ; NEXT_GO = rollout selectif des helper extractions prouvees.

### Documente seulement

- `Airtable Orchestration Layer` : produit cadre et documente, pas encore prouve comme usage runtime borne ; NEXT_GO = `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01`.
- `OpenClaw Docs Library` : lecture et cartographie documentaire seulement ; NEXT_GO = `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01`.
- `Trading Dual Stack V1 / XAUUSD` : framework documente, schemas/config V1 etablis, LAB operationnel mais sans broker reel ; NEXT_GO = `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01`.
- `LocalCMS` : consumer UI externe, cadrage et plan documentes, usage reel a prouver ; NEXT_GO = `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01`.

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
- `remaining_gaps`: maintenir la couverture produit, les guides et les `NEXT_GO` alignes avec les futurs closeouts significatifs.
- `next_go`: maintenance continue via `docs/product/UPDATE_PROTOCOL.md` ; ouvrir un nouveau rescan Atlas seulement si la couverture produit change.
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
- `user_guide`: `docs/product/guides/AIRTABLE_ORCHESTRATION_LAYER_READONLY.md`
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

## DESK_PRO

- `product_name`: Desk Pro
- `parent_branch`: -- (stack multi-composants, pas de branche unique)
- `reason_to_exist`: pipeline operationnel de capture, analyse, execution et visualisation desk trading.
- `final_usage_target`: stack Desk Pro unifiee avec survivant unique, runbooks complets, dashboard produit.
- `usage_view`: `USABLE_LIMITED`
- `current_state`: `USABLE_LIMITED`
- `usable_now`: `limited`
- `operator_read`: utilisable maintenant avec runbooks et wrappers, mais survivant unique non fige et frontiere desk_pro / desk_* en cours de clarification.
- `usage_mode`: usage operationnel via runbooks, wrappers cmd/menu/sanity, script admin reel, dashboard.
- `user_guide`: `docs/product/guides/DESK_PRO.md`
- `canonical_sources`:
  - `docs/status/desk_pro_stack_canonique.md`
  - `docs/desk_pro_multi_machine_quick_reference.md`
  - `docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md`
- `remaining_gaps`: survivant unique non fige, frontiere desk_pro / desk_* en cours de clarification documentaire.
- `next_go`: `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01`
- `do_not_use_notes`: ne pas confondre la coquille `modules/desk_pro/` (gelee) avec la stack operationnelle.

## BOT_VISION

- `product_name`: Bot Vision
- `parent_branch`: -- (pipeline multi-modules)
- `reason_to_exist`: pipeline de capture screenshot -> analyse Vision -> artefacts Desk Pro / Telegram.
- `final_usage_target`: pipeline vision avec survivant unique, capture headless, artefacts Desk Pro/Telegram.
- `usage_view`: `USABLE_LIMITED`
- `current_state`: `USABLE_LIMITED`
- `usable_now`: `limited`
- `operator_read`: paire canonique stable (`vision_bot` + `bot_vision_step2`) avec wrappers unifies, timers et systemd ; `bot_vision` reste legacy preserve.
- `usage_mode`: capture via `vision_bot`, analyse Vision/Telegram et artefacts Desk Pro via `bot_vision_step2`, avec wrappers `cmd-vision` / `menu-vision` / `sanity-vision`.
- `user_guide`: `docs/product/guides/BOT_VISION.md`
- `canonical_sources`:
  - `docs/status/bot_vision_canonique.md`
  - `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`
  - `docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/90_CLOSEOUT.md`
- `remaining_gaps`: verifier l'integrite des timers, du flux inbox -> outbox et la route Telegram `/analyze` avant de parler de surface plus stable.
- `next_go`: `GO_OPT_TRADING_VISION_RUNTIME_STABILIZATION_01`
- `do_not_use_notes`: ne pas utiliser `bot_vision` (legacy) comme surface active.

## DEEPSEEK_STUDENT

- `product_name`: Deepseek Student
- `parent_branch`: -- (surface multi-branches cote `student` / `Local Ollama` / `DeepSeek`)
- `reason_to_exist`: fournir une surface locale d'analyse DeepSeek/Ollama cote `student`, avec wrappers operateur, journalisation et sorties archivees.
- `final_usage_target`: duo local thinking/response stable, accessible via wrappers et/ou API, avec frontiere claire entre surface d'apprentissage locale et orchestrations plus larges.
- `usage_view`: `USABLE_LIMITED`
- `current_state`: `USABLE_LIMITED`
- `usable_now`: `limited`
- `operator_read`: runbook et wrappers existent ; le workspace canonique `student/scripts/` est clarifie, mais le legacy `scripts/student/` reste preserve pour compatibilite.
- `usage_mode`: utiliser `deepseek-student`, `menu-deepseek-student` et `sanity-deepseek-student` pour les analyses locales et la lecture des sorties archivees ; validation externe obligatoire.
- `user_guide`: `docs/product/guides/DEEPSEEK_STUDENT.md`
- `canonical_sources`:
  - `docs/student_deepseek_runbook.md`
  - `docs/status/deepseek_student_canonique.md`
  - `docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_03/90_CLOSEOUT.md`
  - `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_CLOSEOUT.md`
- `remaining_gaps`: dual-layout `student/scripts/` vs `scripts/student/`, verification des callers `post_change.sh` avant tout retrait legacy, OpenClaw lab toujours differe.
- `next_go`: verifier `post_change.sh` avant tout retrait de `scripts/student/` ; ne rouvrir `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01` que si l'integration lab doit reprendre.
- `do_not_use_notes`: surface learning-only ; ne pas l'utiliser comme moteur de decision autonome ni retirer le legacy sans verification.

## TRADINGVIEW_TELEGRAM_ALERT_PIPELINE

- `product_name`: TradingView / Telegram Alert Pipeline
- `parent_branch`: -- (pipeline multi-branches)
- `reason_to_exist`: pipeline de reception d'alertes TradingView -> webhook -> observation -> notification Telegram -> journalisation.
- `final_usage_target`: pipeline complet avec alertes, webhook, Telegram et Desk Pro, boucle fermee.
- `usage_view`: `USABLE_LIMITED`
- `current_state`: `USABLE_LIMITED`
- `usable_now`: `limited`
- `operator_read`: utilisable avec alert webhook en continuite active. Parent observer merged, dry-run bridge packet fonctionnel.
- `usage_mode`: observation TradingView, routage webhook, notification Telegram.
- `user_guide`: `docs/product/guides/TRADINGVIEW_TELEGRAM_PIPELINE.md`
- `canonical_sources`:
  - `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
  - `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/90_CLOSEOUT.md`
- `remaining_gaps`: alert webhook non ferme, export reel et integration Telegram a consolider.
- `next_go`: poursuite GO alert webhook actif puis closeout continuite.
- `do_not_use_notes`: `webhook_server.py` (racine) est un runtime historique, le module canonique est `modules/webhook/`.

## OPENCLAW_RUNTIME

- `product_name`: OpenClaw Runtime
- `parent_branch`: `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- `reason_to_exist`: orchestrer les appels IA via gateway OpenClaw, agents et supervision au-dessus des surfaces trading.
- `final_usage_target`: runtime d'orchestration IA complet avec gateway, agents, supervision et synthese unifiee.
- `usage_view`: `USABLE_LIMITED`
- `current_state`: `USABLE_LIMITED`
- `usable_now`: `limited`
- `operator_read`: modules installables, gateway, cartographie doc (77 sources). TMUX supervision runtime en cours, agents non deployes.
- `usage_mode`: installation et configuration de modules OpenClaw, gateway, supervision TMUX.
- `user_guide`: `docs/product/guides/OPENCLAW_RUNTIME.md`
- `canonical_sources`:
  - `docs/product_targets/OPENCLAW_TARGET_CANON.md`
  - `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/`
  - `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/`
- `remaining_gaps`: orchestration runtime en construction, agents non deployes, synthese unifiee absente.
- `next_go`: `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01`
- `do_not_use_notes`: ne pas confondre avec OpenClaw Docs Library (`DOC_ONLY`, cartographie documentaire).

## DERIVATIVES_COLLECTOR

- `product_name`: derivatives_collector
- `parent_branch`: -- (module canonique)
- `reason_to_exist`: collecter les donnees de marches derives pour le trading, en tant que collecteur canonique.
- `final_usage_target`: collecteur canonique compatible famille collector, avec doctrine, vocabulaire, artifacts et surface operateur alignes.
- `usage_view`: `USABLE_LIMITED`
- `current_state`: `USABLE_LIMITED`
- `usable_now`: `limited`
- `operator_read`: module operationnel multi-versions (V3->V13). La doctrine famille et la separation runtime sont maintenant clarifiees ; la convergence se poursuit sur les extractions utilitaires prouvees.
- `usage_mode`: collecte de donnees marches derives, export JSON/CSV.
- `user_guide`: `docs/product/guides/DERIVATIVES_COLLECTOR.md`
- `canonical_sources`:
  - `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`
  - `docs/COLLECTORS_MIGRATION_MAP_01.md`
  - `docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/90_CLOSEOUT.md`
  - `docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/90_CLOSEOUT.md`
- `remaining_gaps`: rollout selectif des helper extractions, convergence des surfaces operateur et clarification des callers secondaires comme `marketdata` si besoin reel.
- `next_go`: poursuivre le rollout des helper extractions prouvees sans casser la separation runtime.
- `do_not_use_notes`: ne pas forcer la migration runtime immediate vers `collectors_core`.

## TRADING_DUAL_STACK_V1_XAUUSD

- `product_name`: Trading Dual Stack V1 / XAUUSD
- `parent_branch`: -- (framework multi-modules)
- `reason_to_exist`: framework de trading unifie LAB/REALTIME, perimetre XAUUSD borne, avec observation puis validation avant autonomie.
- `final_usage_target`: framework LAB/REALTIME avec broker connecte, ordres papier d'abord, puis reel controle.
- `usage_view`: `DOC_ONLY`
- `current_state`: `DOC_ONLY`
- `usable_now`: `no`
- `operator_read`: schemas/config V1 etablis, LAB operationnel, REALTIME minimale posee. V1 close mais bornee.
- `usage_mode`: lecture du cadre et des schemas. LAB exploitable pour backtest, REALTIME pour observation.
- `user_guide`: `docs/product/guides/TRADING_DUAL_STACK_V1_READONLY.md`
- `canonical_sources`:
  - `docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md`
- `remaining_gaps`: sans broker connecte, sans passage d'ordre reel, sans auto-trading.
- `next_go`: `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` (seulement si besoin d'extension reelle identifie).
- `do_not_use_notes`: ne pas traiter comme un produit live-ready. Aucun ordre reel.

## LOCALCMS

- `product_name`: LocalCMS
- `parent_branch`: -- (projet externe consommateur)
- `reason_to_exist`: consumer UI de opt-trading exploitant /shared, exploration modules, futur cockpit utilisateur.
- `final_usage_target`: consumer UI operationnel avec lecture /shared, exploration modules et cockpit.
- `usage_view`: `DOC_ONLY`
- `current_state`: `DOC_ONLY`
- `usable_now`: `no`
- `operator_read`: cadrage et plan documentes, GO consumer parent ouvert. Projet externe sans runtime integre dans le repo.
- `usage_mode`: lecture du cadrage uniquement. Usage reel a prouver.
- `user_guide`: `docs/product/guides/LOCALCMS_READONLY.md`
- `canonical_sources`:
  - `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/`
  - `docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/`
- `remaining_gaps`: projet externe, pas de runtime integre, usage reel a prouver.
- `next_go`: `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` puis preuve d'usage reel.
- `do_not_use_notes`: ne pas traiter comme un produit integre au repo. Reste un consommateur externe.

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
- `user_guide`: `docs/product/guides/BTC_COINM_DO_NOT_USE_LIVE.md`
- `canonical_sources`:
  - `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md`
  - `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md`
  - `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md`
- `remaining_gaps`: validation utilisateur du parent, formules Bitget, compatibilite, backtest data prep, worker et invariants prouves.
- `next_go`: valider le parent puis ouvrir le child formules dedie avant toute suite runtime.
- `do_not_use_notes`: aucun runtime trading reel, aucun guide live, aucun branchement exchange.

## RISKS

- À qualifier.
