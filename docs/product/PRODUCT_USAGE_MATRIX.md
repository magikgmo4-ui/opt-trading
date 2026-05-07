---
doc_id: OPT_TRADING_PRODUCT_USAGE_MATRIX
doc_type: product_usage_matrix
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/01_USAGE_VIEW.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/02_NEXT_GO_BY_PRODUCT.md
---

# Product Usage Matrix

## Usage View - lecture rapide

| Vue usage | Produits | Lecture operateur |
| --- | --- | --- |
| `USABLE_NOW` | Repo KG | Utilisable maintenant comme projection repo-first, sans le traiter comme source souveraine. |
| `USABLE_LIMITED` | ClickUp Cockpit | Utilisable maintenant pour piloter, avec limites connues et documentees. |
| `DOC_ONLY` | Airtable Orchestration Layer, OpenClaw Docs Library | Lecture et cadrage seulement ; ne pas presenter ces surfaces comme produits runtime finis. |
| `SIMULATED_ONLY` | Botpress Adapter | Simulation et smoke seulement ; pas de lecture live-ready. |
| `FORBIDDEN_LIVE` | BTC COIN-M Accumulation Engine | Aucun usage live ou runtime autorise a ce stade. |

## NEXT_GO par produit

| Produit | Vue usage | NEXT_GO |
| --- | --- | --- |
| ClickUp Cockpit | `USABLE_LIMITED` | Ouvrir un child dedie seulement si besoin reel ou upgrade plan |
| Repo KG | `USABLE_NOW` | `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01` |
| Airtable Orchestration Layer | `DOC_ONLY` | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| Botpress Adapter | `SIMULATED_ONLY` | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |
| OpenClaw Docs Library | `DOC_ONLY` | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` |
| BTC COIN-M Accumulation Engine | `FORBIDDEN_LIVE` | Valider le parent puis ouvrir le child formules dedie |

## Matrice detaillee

| Produit | Branche parent | Vue usage | Produit / role final prevu | Utilisation prevue dans le setup | Etat actuel | Utilisable maintenant ? | Guide utilisateur requis ? | Gap restant vers produit fini | NEXT_GO | Sources canoniques |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ClickUp Cockpit | `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | `USABLE_LIMITED` | Cockpit humain de pilotage des GO, branches, machines, PR, commits, validations et reprises | Piloter les lots actifs et garder une lecture operateur transverse | `USABLE_LIMITED` | Oui, avec limites | Oui | Limites plan gratuit sur statuses, dashboards et template | Ouvrir un child dedie seulement si besoin reel ou upgrade plan | `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/90_CLOSEOUT.md`<br>`docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01/90_CLOSEOUT.md` |
| Repo KG | `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | `USABLE_NOW` | Projection repo-first multi-surfaces via `graph_bundle.json` | Naviguer rapidement entre GO, docs, modules, branches, gaps et resume points | `USABLE_NOW` | Oui | Oui | Etendre la vue usage a plus de produits et modules au-dela du socle initial | `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01` | `docs/chantiers/GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01/10_EXECUTION_SUMMARY.md`<br>`docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01/90_CLOSEOUT.md` |
| Airtable Orchestration Layer | `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | `DOC_ONLY` | Couche legere de journal, review humaine, signaux et exports | Orchestration humaine optionnelle sans remplacer le coeur repo | `DOC_ONLY_READY / GO_LIMITED` | Lecture seulement | Non tant que le bridge produit manque | Bridge repo, tables produit finales, exports et preuve d'usage borne | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` | `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md`<br>`docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md` |
| Botpress Adapter | `go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01` | `SIMULATED_ONLY` | Routeur conversationnel controle entre Telegram, Botpress, OpenClaw et surfaces trading | Classifier les intentions, appliquer la safety gate et retourner un verdict structure | `SIMULATED_PASS` | Simulation seulement | Oui, guide simule seulement | Telegram reel, webhook reel, credentials et smoke production controle | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` | `docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/README.md`<br>`docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01/90_CLOSEOUT.md`<br>`docs/chantiers/GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01/90_CLOSEOUT.md` |
| OpenClaw Docs Library | `go/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01` | `DOC_ONLY` | Librairie de recherche et cartographie documentaire OpenClaw | Lire les surfaces existantes et preparer les futurs GOs OpenClaw | `DOC_ONLY_READY` | Lecture seulement | Oui, guide de lecture | Cartographie raffinee, deep dive composants, synthese finale | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` | `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/00_CADRAGE_PARENT.md`<br>`docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/90_CLOSEOUT.md` |
| BTC COIN-M Accumulation Engine | `go/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01` | `FORBIDDEN_LIVE` | Moteur mathematique puis backtest puis worker borne pour accumulation BTC avec logique COIN-M | Cadrer d'abord le probleme avant toute implementation sensible | `NOT_USABLE_YET / DO_NOT_USE_LIVE` | Non - interdit live | Non, aucun guide live autorise | Validation du parent, formules, compatibilite, backtest et worker | Valider le parent puis ouvrir le child formules dedie | `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md`<br>`docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md` |
