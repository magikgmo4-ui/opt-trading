---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01_CADRAGE
doc_type: cadrage
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/product/UPDATE_PROTOCOL.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/03_USER_GUIDE_MODEL.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01/90_CLOSEOUT.md
---

# 00_CADRAGE - GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01

## 1_MASTER_TARGET

Creer ou completer les guides utilisateur pour les 13 produits du Product Usage Atlas, avec un perimetre strictement borne par le statut reel de chaque produit.

## 2_BASE_STATE

Merge : `8080689` (PR #241, apply repo inventory PASS).

Guides deja existants :
- `CLICKUP_COCKPIT.md` (`USABLE_LIMITED`)
- `REPO_KG.md` (`USABLE_NOW`)
- `BOTPRESS_ADAPTER_SIMULATED.md` (`SIMULATED_ONLY`)
- `OPENCLAW_DOCS_LIBRARY.md` (`DOC_ONLY`)

Produits sans guide :
- Desk Pro, Bot Vision, TradingView / Telegram Alert Pipeline, OpenClaw Runtime, derivatives_collector (USABLE_LIMITED)
- Airtable, Trading Dual Stack V1, LocalCMS (DOC_ONLY)
- BTC COIN-M (FORBIDDEN_LIVE)

## 3_INITIAL_NEED

L'Atlas compte 13 produits, mais seuls 4 ont un guide. Les 9 autres ont besoin d'une documentation d'usage adaptee a leur statut reel, sans creer de guide live pour les surfaces non validees.

## 4_MASTER_PROJECT_PLAN

1. Lire le modele de guide (`03_USER_GUIDE_MODEL.md`).
2. Pour chaque produit sans guide, creer le guide adapte au bucket.
3. Pour les produits avec guide existant, verifier la coherence avec le statut actuel.
4. Mettre a jour `guides/README.md`.
5. Verifier qu'aucun guide ne surestime le produit.

## 7_CANONICAL_STATE

| Bucket | Produits | Guides existants | Guides a creer |
| --- | --- | --- | --- |
| `USABLE_NOW` | Repo KG | Oui | -- |
| `USABLE_LIMITED` | ClickUp, Desk Pro, Bot Vision, TradingView Pipeline, OpenClaw Runtime, derivatives_collector | ClickUp : oui | Desk Pro, Bot Vision, TradingView Pipeline, OpenClaw Runtime, derivatives_collector |
| `DOC_ONLY` | Airtable, OpenClaw Docs, Trading Dual Stack V1, LocalCMS | OpenClaw Docs : oui | Airtable, Trading Dual Stack V1, LocalCMS |
| `SIMULATED_ONLY` | Botpress | Oui | -- |
| `FORBIDDEN_LIVE` | BTC COIN-M | Non | Notice d'interdiction seulement |

## 11_KEY_DECISIONS

- `DOC_ONLY` n'est pas toujours "lecture seulement". Il se subdivise en sous-types selon l'etat reel du produit.
- `SIMULATED_ONLY` n'est pas toujours "test seulement". Il se subdivise selon le niveau de validation et les blocages.
- Chaque guide doit inclure : `1_MASTER_TARGET`, `FINAL_TARGET`, `CURRENT_STATE`, `USAGE_ALLOWED_NOW`, `USAGE_FORBIDDEN_NOW`, `IMPLEMENTATION_PATH`, `CONTINUITY_STATE`, `REPRISE_POINT`, `TODO`, `REMAINING_GAP`, `NEXT_GO`, `PROMOTION_CONDITIONS`.
- Les guides `USABLE_LIMITED` exposent clairement les limites avant usage et le chemin vers le produit fini.
- Les guides `DOC_ONLY` sont adaptes au sous-type : reference (lecture), initial project (reprise), implementation-ready (implementation), blocked (reprise + blocages), archive (ne pas utiliser).
- Les guides `SIMULATED_ONLY` incluent les resultats du smoke/test, la continuite projet, et les conditions de passage vers l'usage reel.
- `BTC COIN-M` recoit une notice d'interdiction avec conditions strictes de deblocage, pas un guide live.
- Chaque guide pointe vers ses sources canoniques et son `NEXT_GO`.

### Sous-types DOC_ONLY

| Sous-type | Sens | Guide adapte |
| --- | --- | --- |
| `DOC_ONLY_REFERENCE` | Closeout, archive, historique, preuve | Guide de lecture |
| `DOC_ONLY_INITIAL_PROJECT` | Document initial de chantier / parent / child | Guide de reprise + continuite |
| `DOC_ONLY_IMPLEMENTATION_READY` | Spec, cadrage, plan pret pour implementation | Guide d'implementation |
| `DOC_ONLY_BLOCKED` | Cadre mais bloque par dependance | Guide de reprise + blocages |
| `DOC_ONLY_ARCHIVE` | Ancien, gele, remplace | Guide archive / ne pas utiliser |

### Sous-types SIMULATED_ONLY

| Sous-type | Sens | Guide adapte |
| --- | --- | --- |
| `SIMULATED_ONLY_TESTED` | Smoke/test valide mais pas reel | Guide de test + resultats |
| `SIMULATED_ONLY_IMPLEMENTATION_READY` | Simulation validee, pret pour le reel | Guide d'implementation reelle + conditions |
| `SIMULATED_ONLY_BLOCKED_EXTERNAL` | Bloque par credentials, webhook, token | Guide de reprise + prerequis externes + conditions de deblocage |
| `SIMULATED_ONLY_DO_NOT_LIVE` | Ne doit pas etre utilise live | Notice securite + conditions de promotion |

## 12_INVARIANTS

- Aucun runtime modifie.
- Aucun secret.
- Aucun guide live pour DOC_ONLY, SIMULATED_ONLY ou FORBIDDEN_LIVE.
- Aucune promotion implicite de produit.
- Chaque guide reflete l'etat prouve, pas une cible future.

## 16_TODO

1. Creer `01_GUIDE_PLAN.md` et `02_GUIDE_COVERAGE_MATRIX.md`.
2. Creer 5 guides `USABLE_LIMITED`.
3. Creer 3 guides `DOC_ONLY` (lecture seule).
4. Creer 1 notice `FORBIDDEN_LIVE`.
5. Mettre a jour `guides/README.md`.
6. Verifier les guides existants.
7. Creer `90_CLOSEOUT.md` et l'entree inbox.

## 17_RESUME_POINT

```text
docs/product/guides/README.md
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01/02_GUIDE_COVERAGE_MATRIX.md
```

## RISKS

- À qualifier.
