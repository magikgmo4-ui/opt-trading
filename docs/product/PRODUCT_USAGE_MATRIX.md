---
doc_id: OPT_TRADING_PRODUCT_USAGE_MATRIX
doc_type: product_usage_matrix
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/01_USAGE_VIEW.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/02_NEXT_GO_BY_PRODUCT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/03_ATLAS_UPDATE_PROPOSAL.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01/01_DELTA_SCAN.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01/90_CLOSEOUT.md
---

# Product Usage Matrix

## Usage View - lecture rapide

| Vue usage | Produits | Lecture operateur |
| --- | --- | --- |
| `USABLE_NOW` | Repo KG | Utilisable maintenant comme projection repo-first, sans le traiter comme source souveraine. |
| `USABLE_LIMITED` | ClickUp Cockpit, Desk Pro, Bot Vision, Deepseek Student, TradingView / Telegram Alert Pipeline, OpenClaw Runtime, derivatives_collector | Utilisable maintenant pour piloter, avec limites connues et documentees. |
| `DOC_ONLY` | Airtable Orchestration Layer, OpenClaw Docs Library, Trading Dual Stack V1 / XAUUSD, LocalCMS | Lecture et cadrage seulement ; ne pas presenter ces surfaces comme produits runtime finis. |
| `SIMULATED_ONLY` | Botpress Adapter | Simulation et smoke seulement ; pas de lecture live-ready. |
| `FORBIDDEN_LIVE` | BTC COIN-M Accumulation Engine | Aucun usage live ou runtime autorise a ce stade. |

## NEXT_GO par produit

| Produit | Vue usage | NEXT_GO |
| --- | --- | --- |
| ClickUp Cockpit | `USABLE_LIMITED` | Ouvrir un child dedie seulement si besoin reel ou upgrade plan |
| Repo KG | `USABLE_NOW` | Maintenance continue via `UPDATE_PROTOCOL.md` ; rescan Atlas si la couverture change |
| Airtable Orchestration Layer | `DOC_ONLY` | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| Botpress Adapter | `SIMULATED_ONLY` | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |
| OpenClaw Docs Library | `DOC_ONLY` | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` |
| BTC COIN-M Accumulation Engine | `FORBIDDEN_LIVE` | Valider le parent puis ouvrir le child formules dedie |
| Desk Pro | `USABLE_LIMITED` | `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` |
| Bot Vision | `USABLE_LIMITED` | `GO_OPT_TRADING_VISION_RUNTIME_STABILIZATION_01` |
| Deepseek Student | `USABLE_LIMITED` | Verifier `post_change.sh` avant tout retrait legacy ; OpenClaw lab reste conditionnel |
| TradingView / Telegram Alert Pipeline | `USABLE_LIMITED` | Poursuite GO alert webhook actif |
| OpenClaw Runtime | `USABLE_LIMITED` | `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` |
| derivatives_collector | `USABLE_LIMITED` | Poursuivre le rollout des helper extractions prouvees |
| Trading Dual Stack V1 / XAUUSD | `DOC_ONLY` | `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` |
| LocalCMS | `DOC_ONLY` | `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` |

## Matrice detaillee

| Produit | Branche parent | Vue usage | Produit / role final prevu | Utilisation prevue dans le setup | Etat actuel | Utilisable maintenant ? | Guide utilisateur requis ? | Gap restant vers produit fini | NEXT_GO | Sources canoniques |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ClickUp Cockpit | `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | `USABLE_LIMITED` | Cockpit humain de pilotage des GO, branches, machines, PR, commits, validations et reprises | Piloter les lots actifs et garder une lecture operateur transverse | `USABLE_LIMITED` | Oui, avec limites | Oui | Limites plan gratuit sur statuses, dashboards et template | Ouvrir un child dedie seulement si besoin reel ou upgrade plan | `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/90_CLOSEOUT.md`<br>`docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01/90_CLOSEOUT.md` |
| Repo KG | `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | `USABLE_NOW` | Projection repo-first multi-surfaces via `graph_bundle.json` | Naviguer rapidement entre GO, docs, modules, branches, gaps et resume points | `USABLE_NOW` | Oui | Oui | Maintenir la couverture produit, les guides et les `NEXT_GO` a mesure que de nouvelles preuves repo arrivent | Maintenance continue via `UPDATE_PROTOCOL.md` ; rescan Atlas si la couverture change | `docs/chantiers/GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01/10_EXECUTION_SUMMARY.md`<br>`docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01/90_CLOSEOUT.md` |
| Airtable Orchestration Layer | `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | `DOC_ONLY` | Couche legere de journal, review humaine, signaux et exports | Orchestration humaine optionnelle sans remplacer le coeur repo | `DOC_ONLY_READY / GO_LIMITED` | Lecture seulement | Oui, guide doc-only | Bridge repo, tables produit finales, exports et preuve d'usage borne | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` | `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md`<br>`docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md` |
| Botpress Adapter | `go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01` | `SIMULATED_ONLY` | Routeur conversationnel controle entre Telegram, Botpress, OpenClaw et surfaces trading | Classifier les intentions, appliquer la safety gate et retourner un verdict structure | `SIMULATED_PASS` | Simulation seulement | Oui, guide simule seulement | Telegram reel, webhook reel, credentials et smoke production controle | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` | `docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/README.md`<br>`docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01/90_CLOSEOUT.md`<br>`docs/chantiers/GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01/90_CLOSEOUT.md` |
| OpenClaw Docs Library | `go/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01` | `DOC_ONLY` | Librairie de recherche et cartographie documentaire OpenClaw | Lire les surfaces existantes et preparer les futurs GOs OpenClaw | `DOC_ONLY_READY` | Lecture seulement | Oui, guide de lecture | Cartographie raffinee, deep dive composants, synthese finale | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` | `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/00_CADRAGE_PARENT.md`<br>`docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/90_CLOSEOUT.md` |
| BTC COIN-M Accumulation Engine | `go/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01` | `FORBIDDEN_LIVE` | Moteur mathematique puis backtest puis worker borne pour accumulation BTC avec logique COIN-M | Cadrer d'abord le probleme avant toute implementation sensible | `NOT_USABLE_YET / DO_NOT_USE_LIVE` | Non - interdit live | Oui, notice d'interdiction | Validation du parent, formules, compatibilite, backtest et worker | Valider le parent puis ouvrir le child formules dedie | `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md`<br>`docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md` |
| Desk Pro | -- | `USABLE_LIMITED` | Stack operationnelle de capture, analyse, execution et visualisation desk | Piloter le desk trading avec runbooks, wrappers, dashboard et script admin | `USABLE_LIMITED` | Oui, avec limites | Oui | Survivant unique non fige, frontiere desk_pro / desk_* en cours de clarification | `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` | `docs/status/desk_pro_stack_canonique.md`<br>`docs/desk_pro_multi_machine_quick_reference.md`<br>`docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md` |
| Bot Vision | -- | `USABLE_LIMITED` | Pipeline capture screenshot -> analyse Vision -> artefacts Desk Pro / Telegram | Capturer et analyser des screenshots trading, produire des artefacts exploitables | `USABLE_LIMITED` | Oui, paire canonique stable mais encore bornee | Oui | Timers, inbox/outbox et route Telegram `/analyze` a stabiliser ; legacy `bot_vision` encore preserve | `GO_OPT_TRADING_VISION_RUNTIME_STABILIZATION_01` | `docs/status/bot_vision_canonique.md`<br>`docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`<br>`docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/90_CLOSEOUT.md` |
| Deepseek Student | -- | `USABLE_LIMITED` | Surface locale d'analyse DeepSeek/Ollama cote `student` | Lancer des analyses locales, des rapports quotidiens et consulter des sorties archivees via wrappers student | `USABLE_LIMITED` | Oui, avec limites | Oui | Dual-layout canonical/legacy, verification `post_change.sh` avant retrait legacy, OpenClaw lab differe | Verifier `post_change.sh` avant tout retrait legacy ; OpenClaw lab reste conditionnel | `docs/student_deepseek_runbook.md`<br>`docs/status/deepseek_student_canonique.md`<br>`docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_03/90_CLOSEOUT.md`<br>`docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_CLOSEOUT.md` |
| TradingView / Telegram Alert Pipeline | -- | `USABLE_LIMITED` | Pipeline d'alertes TradingView -> webhook -> observation -> Telegram | Recevoir et router les alertes TradingView avec observation et notification | `USABLE_LIMITED` | Oui, alert webhook en continuite | Oui | Alert webhook non ferme, export reel et integration Telegram a consolider | Poursuite GO alert webhook actif | `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`<br>`docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/90_CLOSEOUT.md` |
| OpenClaw Runtime | -- | `USABLE_LIMITED` | Orchestration IA controlee au-dessus des surfaces trading | Orchestrer les appels IA via gateway, agents et supervision | `USABLE_LIMITED` | Oui, modules installables et gateway | Oui | Orchestration runtime en construction, agents non deployes, synthese unifiee absente | `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` | `docs/product_targets/OPENCLAW_TARGET_CANON.md`<br>`docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/` |
| derivatives_collector | -- | `USABLE_LIMITED` | Collecteur canonique de donnees marches derives | Collecter les donnees marches derives pour le trading | `USABLE_LIMITED` | Oui, module operationnel multi-versions | Oui | Doctrine famille alignee ; helper extractions selectives et convergence surface operateur restent en cours | Poursuivre le rollout des helper extractions prouvees | `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`<br>`docs/COLLECTORS_MIGRATION_MAP_01.md`<br>`docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/90_CLOSEOUT.md`<br>`docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/90_CLOSEOUT.md` |
| Trading Dual Stack V1 / XAUUSD | -- | `DOC_ONLY` | Framework LAB/REALTIME unifie, perimetre XAUUSD borne | Tester des strategies en LAB, observer en REALTIME sans ordre reel | `DOC_ONLY` | Non runtime | Oui, guide doc-only | Sans broker, sans ordre reel, sans auto-trading. V1 close mais bornee. | `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` | `docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md` |
| LocalCMS | -- | `DOC_ONLY` | Consumer UI de opt-trading exploitant /shared | Lire les surfaces partagees et servir de cockpit utilisateur futur | `DOC_ONLY` | Non runtime | Oui, guide doc-only | Projet externe, pas de runtime integre, usage reel a prouver | `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/`<br>`docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/` |

## RISKS

- À qualifier.
