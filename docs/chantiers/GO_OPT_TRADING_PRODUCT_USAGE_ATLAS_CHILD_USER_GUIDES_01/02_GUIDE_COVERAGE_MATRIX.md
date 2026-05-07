---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01_GUIDE_COVERAGE_MATRIX
doc_type: coverage_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product/guides/README.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
---

# 02_GUIDE_COVERAGE_MATRIX - Couverture des guides (v2 avec sous-types)

| Produit | Bucket | Sous-type | Guide | 1_MASTER_TARGET | IMPLEMENTATION_PATH | CONTINUITY_STATE | REPRISE_POINT | PROMOTION_CONDITIONS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Repo KG | `USABLE_NOW` | Usage reel read-only | `REPO_KG.md` | Oui | N/A | N/A | Oui | N/A |
| ClickUp Cockpit | `USABLE_LIMITED` | Usage limite | `CLICKUP_COCKPIT.md` | Oui | N/A | N/A | Oui | Oui |
| Desk Pro | `USABLE_LIMITED` | Usage limite / continuite | `DESK_PRO.md` | Oui | Oui | Oui | Oui | Oui |
| Bot Vision | `USABLE_LIMITED` | Pipeline transitoire | `BOT_VISION.md` | Oui | Oui | Oui | Oui | Oui |
| TradingView / Telegram Alert Pipeline | `USABLE_LIMITED` | Pipeline partiel | `TRADINGVIEW_TELEGRAM_PIPELINE.md` | Oui | Oui | Oui | Oui | Oui |
| OpenClaw Runtime | `USABLE_LIMITED` | Runtime en construction | `OPENCLAW_RUNTIME.md` | Oui | Oui | Oui | Oui | Oui |
| derivatives_collector | `USABLE_LIMITED` | Module / convergence | `DERIVATIVES_COLLECTOR.md` | Oui | Oui | Oui | Oui | Oui |
| Airtable Orchestration Layer | `DOC_ONLY` | `DOC_ONLY_IMPLEMENTATION_READY` | `AIRTABLE_ORCHESTRATION_LAYER_READONLY.md` | Oui | Oui | Oui | Oui | Oui |
| OpenClaw Docs Library | `DOC_ONLY` | `DOC_ONLY_REFERENCE` | `OPENCLAW_DOCS_LIBRARY.md` | Partiel | Partiel | Partiel | Oui | Partiel |
| Trading Dual Stack V1 / XAUUSD | `DOC_ONLY` | `DOC_ONLY_INITIAL_PROJECT` | `TRADING_DUAL_STACK_V1_READONLY.md` | Oui | Oui | Oui | Oui | Oui |
| LocalCMS | `DOC_ONLY` | `DOC_ONLY_IMPLEMENTATION_READY` | `LOCALCMS_READONLY.md` | Oui | Oui | Oui | Oui | Oui |
| Botpress Adapter | `SIMULATED_ONLY` | `SIMULATED_ONLY_IMPLEMENTATION_READY` | `BOTPRESS_ADAPTER_SIMULATED.md` | Oui | Oui | Oui | Oui | Oui |
| BTC COIN-M Accumulation Engine | `FORBIDDEN_LIVE` | Interdiction forte | `BTC_COINM_DO_NOT_USE_LIVE.md` | Oui | N/A | N/A | N/A | Oui |

## Verifications

| Produit | Dit quand ne pas utiliser | Sources canoniques | NEXT_GO | Surestime le produit ? |
| --- | --- | --- | --- | --- |
| Tous | Oui | Oui | Oui | Non |
