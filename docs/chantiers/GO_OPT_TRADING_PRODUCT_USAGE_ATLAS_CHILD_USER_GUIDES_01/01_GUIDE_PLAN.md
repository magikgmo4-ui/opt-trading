---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01_GUIDE_PLAN
doc_type: guide_plan
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/03_USER_GUIDE_MODEL.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
---

# 01_GUIDE_PLAN - Plan de couverture

## Regles par bucket

| Bucket | Type de guide | Contenu cle |
| --- | --- | --- |
| `USABLE_NOW` | Guide complet | Usage, limites, depannage, sources, NEXT_GO |
| `USABLE_LIMITED` | Guide avec limites explicites | Usage, limites connues, quand ne pas utiliser, NEXT_GO |
| `DOC_ONLY` | Guide de lecture seule | Ce que c'est, comment le lire, ce qu'il ne faut pas en deduire, NEXT_GO |
| `SIMULATED_ONLY` | Guide de simulation | Perimetre simule, quand ne pas utiliser en live, NEXT_GO |
| `FORBIDDEN_LIVE` | Notice d'interdiction | Interdiction explicite, raison, condition de levee, aucun usage |

## Structure standard (adaptee par bucket)

```text
# Guide - <Produit>

## Ce que c'est
## A quoi ca sert
## Quand l'utiliser
## Quand ne pas l'utiliser
## Prerequis
## Commandes / acces
## Procedure simple
## Verification PASS
## Limites
## Depannage
## Source canonique
## NEXT_GO
```

Pour les guides `DOC_ONLY` : remplacer "Quand l'utiliser" par "Quand le consulter", et "Procedure simple" par "Procedure de lecture".

Pour les guides `SIMULATED_ONLY` : ajouter une section "Ce que ce guide ne couvre pas".

## Actions

| Produit | Action | Fichier |
| --- | --- | --- |
| Repo KG | Verifier | `REPO_KG.md` (existant) |
| ClickUp Cockpit | Verifier | `CLICKUP_COCKPIT.md` (existant) |
| Desk Pro | Creer | `DESK_PRO.md` |
| Bot Vision | Creer | `BOT_VISION.md` |
| TradingView / Telegram Alert Pipeline | Creer | `TRADINGVIEW_TELEGRAM_PIPELINE.md` |
| OpenClaw Runtime | Creer | `OPENCLAW_RUNTIME.md` |
| derivatives_collector | Creer | `DERIVATIVES_COLLECTOR.md` |
| Airtable Orchestration Layer | Creer | `AIRTABLE_ORCHESTRATION_LAYER_READONLY.md` |
| OpenClaw Docs Library | Verifier | `OPENCLAW_DOCS_LIBRARY.md` (existant) |
| Trading Dual Stack V1 / XAUUSD | Creer | `TRADING_DUAL_STACK_V1_READONLY.md` |
| LocalCMS | Creer | `LOCALCMS_READONLY.md` |
| Botpress Adapter | Verifier | `BOTPRESS_ADAPTER_SIMULATED.md` (existant) |
| BTC COIN-M Accumulation Engine | Creer | `BTC_COINM_DO_NOT_USE_LIVE.md` |
| README | Mettre a jour | `README.md` |
