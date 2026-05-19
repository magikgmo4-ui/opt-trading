---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01_NEXT_GO_BY_PRODUCT
doc_type: next_go_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/FINAL_TARGET_GAPS.md
---

# 02_NEXT_GO_BY_PRODUCT - Suite par produit

## Matrice

| Produit | Vue usage | Gap principal | NEXT_GO |
| --- | --- | --- | --- |
| ClickUp Cockpit | `USABLE_LIMITED` | Limites plan gratuit sur statuses, dashboards et template | Ouvrir un child dedie seulement si besoin reel ou upgrade plan |
| Repo KG | `USABLE_NOW` | Couverture produit encore limitee au socle initial | `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01` |
| Airtable Orchestration Layer | `DOC_ONLY` | Bridge repo, tables finales, exports et preuve d'usage borne | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| Botpress Adapter | `SIMULATED_ONLY` | Telegram reel, webhook reel, credentials et smoke production controle | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |
| OpenClaw Docs Library | `DOC_ONLY` | Cartographie raffinee, deep dive composants, synthese finale | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` |
| BTC COIN-M Accumulation Engine | `FORBIDDEN_LIVE` | Validation du parent, formules et invariants avant toute suite | Valider le parent puis ouvrir le child formules dedie |

## Regle

Chaque produit doit pointer vers :
- un `NEXT_GO` explicite ; ou
- une condition d'ouverture claire quand aucun GO ne doit etre force artificiellement.
