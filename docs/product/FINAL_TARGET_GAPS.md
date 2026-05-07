---
doc_id: OPT_TRADING_FINAL_TARGET_GAPS
doc_type: gap_matrix
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/01_USAGE_VIEW.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/02_NEXT_GO_BY_PRODUCT.md
---

# Final Target Gaps

## Principe

Ce document dit pourquoi un produit n'est pas encore `PRODUCT_FINISHED`, meme quand un ou plusieurs chantiers sont PASS.

## Lecture par vue usage

| Vue usage | Produits | Sens du gap |
| --- | --- | --- |
| `USABLE_NOW` | Repo KG | Le gap sert a enrichir la lecture produit, pas a debloquer un usage deja absent. |
| `USABLE_LIMITED` | ClickUp Cockpit | Le gap sert a fermer des limites non bloquantes pour l'usage courant. |
| `DOC_ONLY` | Airtable Orchestration Layer, OpenClaw Docs Library | Le gap sert a passer d'une lecture documentaire a une preuve d'usage plus concrete. |
| `SIMULATED_ONLY` | Botpress Adapter | Le gap sert a passer de la simulation vers un reel controle. |
| `FORBIDDEN_LIVE` | BTC COIN-M Accumulation Engine | Le gap sert d'abord a maintenir l'interdiction live tant que les preuves manquent. |

## Gaps par produit

| Produit | Vue usage | Pourquoi ce n'est pas fini | Gap critique | NEXT_GO |
| --- | --- | --- | --- | --- |
| ClickUp Cockpit | `USABLE_LIMITED` | Le cockpit marche, mais le plan gratuit borne encore des parties de l'usage cible | Statuses, dashboards et template restent incomplets | Ouvrir un child dedie seulement si besoin reel ou upgrade plan |
| Repo KG | `USABLE_NOW` | La projection est exploitable, mais la couverture produit reste bornee au socle initial | Etendre la vue usage a plus de produits et modules du repo | `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01` |
| Airtable Orchestration Layer | `DOC_ONLY` | Le produit est bien cadre, mais le bridge repo et la preuve d'usage produit manquent | `modules/airtable_bridge/` + tables finales + exports | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| Botpress Adapter | `SIMULATED_ONLY` | La simulation est prouvee, pas l'usage reel complet | Telegram reel + webhook reel + credentials hors repo | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |
| OpenClaw Docs Library | `DOC_ONLY` | La cartographie parent existe, pas encore la lecture finale unifiee | Raffinement de cartographie puis synthese finale | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` |
| BTC COIN-M Accumulation Engine | `FORBIDDEN_LIVE` | Le cadrage est draft et interdit tout usage live | Validation du parent, formules et invariants avant toute suite | Valider le parent puis ouvrir le child formules dedie |

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
