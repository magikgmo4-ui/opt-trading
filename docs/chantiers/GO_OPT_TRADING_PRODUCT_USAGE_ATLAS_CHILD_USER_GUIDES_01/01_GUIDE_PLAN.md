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
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# 01_GUIDE_PLAN - Plan de couverture (v2 avec sous-types)

## Structure de guide enrichie

Chaque guide doit contenir au minimum :

```text
# Guide - <Produit>

## 1_MASTER_TARGET
## FINAL_TARGET
## CURRENT_STATE
## USAGE_ALLOWED_NOW
## USAGE_FORBIDDEN_NOW
## IMPLEMENTATION_PATH
## CONTINUITY_STATE (actif / en reprise / bloque / archive)
## MACHINE / SURFACE concernee
## REPRISE_POINT
## TODO
## REMAINING_GAP
## NEXT_GO
## PROMOTION_CONDITIONS
## Ce que c'est
## A quoi ca sert
## Quand l'utiliser / le consulter
## Quand ne pas l'utiliser
## Prerequis
## Commandes / acces
## Procedure simple
## Verification PASS
## Limites
## Depannage
## Source canonique
```

## Regles par sous-type

### DOC_ONLY_REFERENCE (Closeout, archive, preuve)
- Guide de lecture uniquement.
- Pas d'implementation path.
- USAGE_ALLOWED_NOW = lecture seulement.
- USAGE_FORBIDDEN_NOW = usage runtime.

### DOC_ONLY_INITIAL_PROJECT (Document initial de chantier)
- Guide de reprise + continuite.
- IMPLEMENTATION_PATH = etapes restantes du chantier.
- CONTINUITY_STATE = actif / en reprise.
- REPRISE_POINT obligatoire.

### DOC_ONLY_IMPLEMENTATION_READY (Spec, plan pret)
- Guide d'implementation autorise.
- IMPLEMENTATION_PATH = etapes concretes.
- PROMOTION_CONDITIONS explicites.

### DOC_ONLY_BLOCKED (Bloque par dependance)
- Guide de reprise + blocages.
- USAGE_FORBIDDEN_NOW = raison du blocage.
- PROMOTION_CONDITIONS = conditions de deblocage.

### DOC_ONLY_ARCHIVE (Ancien, gele)
- Guide archive / ne pas utiliser.
- USAGE_FORBIDDEN_NOW = tout usage.
- NEXT_GO = aucun.

### SIMULATED_ONLY_TESTED (Smoke valide)
- Guide de test + resultats.
- Inclure les resultats du smoke/test.
- IMPLEMENTATION_PATH = etapes vers le reel.

### SIMULATED_ONLY_IMPLEMENTATION_READY (Pret pour reel)
- Guide d'implementation reelle + conditions.
- PROMOTION_CONDITIONS = etapes de validation du reel.
- Inclure TODO et NEXT_GO.

### SIMULATED_ONLY_BLOCKED_EXTERNAL (Credentials, webhook)
- Guide de reprise + prerequis externes.
- USAGE_FORBIDDEN_NOW = dependances externes manquantes.
- PROMOTION_CONDITIONS = obtention des credentials/webhooks.

## Classification par produit

| Produit | Bucket | Sous-type | Guide |
| --- | --- | --- | --- |
| Repo KG | `USABLE_NOW` | Usage reel read-only | `REPO_KG.md` (existant) |
| ClickUp Cockpit | `USABLE_LIMITED` | Usage limite | `CLICKUP_COCKPIT.md` (existant) |
| Desk Pro | `USABLE_LIMITED` | Usage limite / continuite produit | `DESK_PRO.md` (a enrichir) |
| Bot Vision | `USABLE_LIMITED` | Pipeline transitoire | `BOT_VISION.md` (a enrichir) |
| TradingView / Telegram Alert Pipeline | `USABLE_LIMITED` | Pipeline partiel | `TRADINGVIEW_TELEGRAM_PIPELINE.md` (a enrichir) |
| OpenClaw Runtime | `USABLE_LIMITED` | Runtime en construction | `OPENCLAW_RUNTIME.md` (a enrichir) |
| derivatives_collector | `USABLE_LIMITED` | Module operationnel / convergence | `DERIVATIVES_COLLECTOR.md` (a enrichir) |
| Airtable Orchestration Layer | `DOC_ONLY` | `DOC_ONLY_IMPLEMENTATION_READY` | `AIRTABLE_ORCHESTRATION_LAYER_READONLY.md` (a enrichir) |
| OpenClaw Docs Library | `DOC_ONLY` | `DOC_ONLY_REFERENCE` + `DOC_ONLY_IMPLEMENTATION_READY` | `OPENCLAW_DOCS_LIBRARY.md` (existant, a verifier) |
| Trading Dual Stack V1 / XAUUSD | `DOC_ONLY` | `DOC_ONLY_INITIAL_PROJECT` | `TRADING_DUAL_STACK_V1_READONLY.md` (a enrichir) |
| LocalCMS | `DOC_ONLY` | `DOC_ONLY_IMPLEMENTATION_READY` | `LOCALCMS_READONLY.md` (a enrichir) |
| Botpress Adapter | `SIMULATED_ONLY` | `SIMULATED_ONLY_IMPLEMENTATION_READY` | `BOTPRESS_ADAPTER_SIMULATED.md` (a enrichir) |
| BTC COIN-M Accumulation Engine | `FORBIDDEN_LIVE` | Interdiction forte | `BTC_COINM_DO_NOT_USE_LIVE.md` (existant, a verifier) |

## Actions planifiees

| Fichier | Action | Priorite |
| --- | --- | --- |
| `REPO_KG.md` | Verifier structure enrichie | Haute |
| `CLICKUP_COCKPIT.md` | Verifier structure enrichie | Haute |
| `DESK_PRO.md` | Enrichir (MASTER_TARGET, IMPLEMENTATION_PATH, CONTINUITY_STATE, etc.) | Haute |
| `BOT_VISION.md` | Enrichir | Haute |
| `TRADINGVIEW_TELEGRAM_PIPELINE.md` | Enrichir | Haute |
| `OPENCLAW_RUNTIME.md` | Enrichir | Haute |
| `DERIVATIVES_COLLECTOR.md` | Enrichir | Haute |
| `AIRTABLE_ORCHESTRATION_LAYER_READONLY.md` | Reclasser en IMPLEMENTATION_READY + enrichir | Haute |
| `OPENCLAW_DOCS_LIBRARY.md` | Verifier et enrichir si necessaire | Moyenne |
| `TRADING_DUAL_STACK_V1_READONLY.md` | Reclasser en INITIAL_PROJECT + enrichir | Haute |
| `LOCALCMS_READONLY.md` | Reclasser en IMPLEMENTATION_READY + enrichir | Haute |
| `BOTPRESS_ADAPTER_SIMULATED.md` | Reclasser en IMPLEMENTATION_READY + enrichir | Haute |
| `BTC_COINM_DO_NOT_USE_LIVE.md` | Verifier conditions de deblocage | Moyenne |
| `README.md` | Mettre a jour la table de couverture | Haute |

## RISKS

- À qualifier.
