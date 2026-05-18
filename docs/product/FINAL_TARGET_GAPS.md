---
doc_id: OPT_TRADING_FINAL_TARGET_GAPS
doc_type: gap_matrix
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/01_USAGE_VIEW.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/02_NEXT_GO_BY_PRODUCT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01/01_DELTA_SCAN.md
---

# Final Target Gaps

## Principe

Ce document dit pourquoi un produit n'est pas encore `PRODUCT_FINISHED`, meme quand un ou plusieurs chantiers sont PASS.

## Lecture par vue usage

| Vue usage | Produits | Sens du gap |
| --- | --- | --- |
| `USABLE_NOW` | Repo KG | Le gap sert a enrichir la lecture produit, pas a debloquer un usage deja absent. |
| `USABLE_LIMITED` | ClickUp Cockpit, Desk Pro, Bot Vision, Deepseek Student, TradingView Pipeline, OpenClaw Runtime, derivatives_collector | Le gap sert a fermer des limites non bloquantes ou a consolider la structure. |
| `DOC_ONLY` | Airtable Orchestration Layer, OpenClaw Docs Library, Trading Dual Stack V1, LocalCMS | Le gap sert a passer d'une lecture documentaire a une preuve d'usage plus concrete. |
| `SIMULATED_ONLY` | Botpress Adapter | Le gap sert a passer de la simulation vers un reel controle. |
| `FORBIDDEN_LIVE` | BTC COIN-M Accumulation Engine | Le gap sert d'abord a maintenir l'interdiction live tant que les preuves manquent. |

## Gaps par produit

| Produit | Vue usage | Pourquoi ce n'est pas fini | Gap critique | NEXT_GO |
| --- | --- | --- | --- | --- |
| ClickUp Cockpit | `USABLE_LIMITED` | Le cockpit marche, mais le plan gratuit borne encore des parties de l'usage cible | Statuses, dashboards et template restent incomplets | Ouvrir un child dedie seulement si besoin reel ou upgrade plan |
| Repo KG | `USABLE_NOW` | La projection est exploitable, la couverture produit est elargie par l'inventaire | Maintenir les guides utilisateur et la couverture produit apres application | `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01` |
| Airtable Orchestration Layer | `DOC_ONLY` | Le produit est bien cadre, mais le bridge repo et la preuve d'usage produit manquent | `modules/airtable_bridge/` + tables finales + exports | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| Botpress Adapter | `SIMULATED_ONLY` | La simulation est prouvee, pas l'usage reel complet | Telegram reel + webhook reel + credentials hors repo | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |
| OpenClaw Docs Library | `DOC_ONLY` | La cartographie parent existe, pas encore la lecture finale unifiee | Raffinement de cartographie puis synthese finale | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` |
| BTC COIN-M Accumulation Engine | `FORBIDDEN_LIVE` | Le cadrage est draft et interdit tout usage live | Validation du parent, formules et invariants avant toute suite | Valider le parent puis ouvrir le child formules dedie |
| Desk Pro | `USABLE_LIMITED` | Stack operationnelle, mais survivant unique non fige et frontiere desk_pro/desk_* floue | Consolidation structurelle de la stack Desk Pro | `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` |
| Bot Vision | `USABLE_LIMITED` | La paire runtime est maintenant claire, mais la stabilisation operatoire n'est pas fermee | Timers, inbox/outbox et route Telegram `/analyze` a stabiliser ; legacy `bot_vision` encore preserve | `GO_OPT_TRADING_VISION_RUNTIME_STABILIZATION_01` |
| Deepseek Student | `USABLE_LIMITED` | Surface locale exploitable, mais encore bornee par un dual-layout et une frontiere lab non fermee | Verifier `post_change.sh` avant tout retrait legacy ; OpenClaw lab reste differe et externe a ce lot | Verification `post_change.sh` avant retrait legacy ; qualification lab seulement si besoin explicite |
| TradingView / Telegram Alert Pipeline | `USABLE_LIMITED` | Pipeline actif, mais alert webhook non ferme et integration Telegram partielle | Closeout alert webhook, export reel, integration Telegram | Poursuite GO alert webhook actif |
| OpenClaw Runtime | `USABLE_LIMITED` | Modules installables et gateway operationnels, mais orchestration incomplete | Agents non deployes, synthese runtime unifiee absente | `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` |
| derivatives_collector | `USABLE_LIMITED` | Le collecteur est canonique, mais la convergence famille n'est pas totalement fermee | Rollout selectif des helper extractions et convergence surface operateur / callers secondaires | Poursuivre le rollout des helper extractions prouvees |
| Trading Dual Stack V1 / XAUUSD | `DOC_ONLY` | Framework documente, LAB operationnel, mais sans broker reel | Broker connecte, ordres papier, validation avant reel | `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` |
| LocalCMS | `DOC_ONLY` | Cadrage et plan documentes, mais projet externe sans runtime integre | Preuve d'usage reel, integration runtime | `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` |

## Interdits explicites

- Ne pas presenter Airtable comme un runtime produit fini.
- Ne pas presenter Botpress comme live-ready.
- Ne pas presenter OpenClaw docs comme un wiki final ou une orchestration runtime.
- Ne pas presenter BTC COIN-M comme utilisable maintenant.

## Ce qui est deja utile maintenant

- ClickUp pour piloter avec limites.
- Repo KG pour naviguer le repo.
- Botpress pour tester un flux simule borne.
- OpenClaw docs pour lire et reperer les surfaces.
- Desk Pro pour operer le desk trading.
- Bot Vision pour capturer et analyser des screenshots.
- Deepseek Student pour lancer des analyses locales cote `student` avec validation externe.
- TradingView Pipeline pour recevoir et router les alertes.
- OpenClaw Runtime pour installer et configurer la gateway.
- derivatives_collector pour collecter les donnees marches derives.
