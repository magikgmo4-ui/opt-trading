---
doc_id: OPT_TRADING_PRODUCT_GUIDES_README
doc_type: guides_index
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product/PRODUCT_USAGE_MATRIX.md
---

# Guides README

## Guides disponibles

| Guide | Portee | Bucket | Sous-type |
| --- | --- | --- | --- |
| `REPO_KG.md` | Guide d'usage repo-first du Repo KG | `USABLE_NOW` | Usage reel read-only |
| `CLICKUP_COCKPIT.md` | Guide d'usage humain du cockpit ClickUp | `USABLE_LIMITED` | Usage limite |
| `DESK_PRO.md` | Guide d'usage de la stack Desk Pro | `USABLE_LIMITED` | Usage limite / continuite produit |
| `BOT_VISION.md` | Guide d'usage du pipeline Bot Vision | `USABLE_LIMITED` | Pipeline transitoire |
| `TRADINGVIEW_TELEGRAM_PIPELINE.md` | Guide d'usage du pipeline TradingView / Telegram | `USABLE_LIMITED` | Pipeline partiel |
| `OPENCLAW_RUNTIME.md` | Guide d'usage du runtime OpenClaw | `USABLE_LIMITED` | Runtime en construction |
| `DERIVATIVES_COLLECTOR.md` | Guide d'usage du derivatives_collector | `USABLE_LIMITED` | Module operationnel / convergence |
| `AIRTABLE_ORCHESTRATION_LAYER_READONLY.md` | Guide d'implementation Airtable | `DOC_ONLY` | `DOC_ONLY_IMPLEMENTATION_READY` |
| `OPENCLAW_DOCS_LIBRARY.md` | Guide de lecture de la librairie documentaire OpenClaw | `DOC_ONLY` | `DOC_ONLY_REFERENCE` |
| `TRADING_DUAL_STACK_V1_READONLY.md` | Guide de reprise Trading Dual Stack V1 | `DOC_ONLY` | `DOC_ONLY_INITIAL_PROJECT` |
| `LOCALCMS_READONLY.md` | Guide d'implementation LocalCMS | `DOC_ONLY` | `DOC_ONLY_IMPLEMENTATION_READY` |
| `BOTPRESS_ADAPTER_SIMULATED.md` | Guide d'implementation Botpress | `SIMULATED_ONLY` | `SIMULATED_ONLY_IMPLEMENTATION_READY` |
| `BTC_COINM_DO_NOT_USE_LIVE.md` | Notice d'interdiction BTC COIN-M | `FORBIDDEN_LIVE` | Interdiction forte |

## Types de guides

| Type | Nombre | Sous-types |
| --- | --- | --- |
| Guide complet | 1 | `USABLE_NOW` |
| Guide avec limites | 6 | `USABLE_LIMITED` |
| Guide d'implementation / reprise / lecture | 4 | `DOC_ONLY_REFERENCE`, `DOC_ONLY_INITIAL_PROJECT`, `DOC_ONLY_IMPLEMENTATION_READY` |
| Guide d'implementation reelle | 1 | `SIMULATED_ONLY_IMPLEMENTATION_READY` |
| Notice d'interdiction | 1 | `FORBIDDEN_LIVE` |

## Regle

Un guide reflete l'etat prouve aujourd'hui, pas une cible future.
Chaque guide inclut : `1_MASTER_TARGET`, `FINAL_TARGET`, `CURRENT_STATE`, `IMPLEMENTATION_PATH`, `CONTINUITY_STATE`, `REPRISE_POINT`, `TODO`, `REMAINING_GAP`, `NEXT_GO`, `PROMOTION_CONDITIONS`.
Les guides `DOC_ONLY` sont adaptes au sous-type reel du produit (pas "lecture seulement" par defaut).
Les guides `SIMULATED_ONLY` incluent le chemin vers l'usage reel.
