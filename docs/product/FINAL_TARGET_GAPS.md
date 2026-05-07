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
---

# Final Target Gaps

## Principe

Ce document dit pourquoi un produit n'est pas encore `PRODUCT_FINISHED`, meme quand un ou plusieurs chantiers sont PASS.

## Gaps par produit

| Produit | Pourquoi ce n'est pas fini | Gap critique | NEXT_GO |
| --- | --- | --- | --- |
| ClickUp Cockpit | Le cockpit marche, mais le plan gratuit borne encore des parties de l'usage cible | Statuses, dashboards et template restent incomplets | Ouvrir un child dedie seulement si besoin reel ou upgrade plan |
| Repo KG | La projection est exploitable, mais la lecture produit complete depend encore d'un overlay explicite | Vue produit / usage reel a maintenir au-dessus du bundle | `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01` |
| Airtable Orchestration Layer | Le produit est bien cadre, mais le bridge repo et la preuve d'usage produit manquent | `modules/airtable_bridge/` + tables finales + exports | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| Botpress Adapter | La simulation est prouvee, pas l'usage reel complet | Telegram reel + webhook reel + credentials hors repo | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |
| OpenClaw Docs Library | La cartographie parent existe, pas encore la lecture finale unifiee | Raffinement de cartographie puis synthese finale | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` |
| BTC COIN-M Accumulation Engine | Le cadrage est draft et interdit tout usage live | Validation du parent, formules et invariants avant toute suite | Valider le parent puis ouvrir le child formules dedie |

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
