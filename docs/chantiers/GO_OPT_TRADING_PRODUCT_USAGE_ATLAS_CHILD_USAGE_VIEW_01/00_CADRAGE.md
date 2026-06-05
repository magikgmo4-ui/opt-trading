---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01_CADRAGE
doc_type: cadrage
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01
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
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/90_CLOSEOUT.md
---

# 00_CADRAGE - GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01

## 1_MASTER_TARGET

Enrichir la couche Product Usage Atlas avec une vue d'usage operateur plus directe, afin de lire sans ambiguite :
- ce qui est utilisable maintenant ;
- ce qui est utilisable avec limites ;
- ce qui est seulement doc-only ;
- ce qui est seulement simule ;
- ce qui est interdit live ;
- le NEXT_GO par produit.

## 2_BASE_STATE

Point de depart : `sot/mainline` au merge `570a2dd`, qui integre deja le parent `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01`.

## 3_INITIAL_NEED

Le parent a cree l'Atlas, la matrice, les guides et les gaps.

Le besoin courant est d'ajouter une lecture plus immediate, orientee usage reel, au-dessus des statuts produit deja documentes.

## 4_MASTER_PROJECT_PLAN

1. Definir une vue d'usage canonique bornee.
2. Ajouter une lecture rapide par buckets dans `PRODUCT_USAGE_MATRIX.md`.
3. Ajouter la meme lecture dans `PRODUCT_USAGE_ATLAS.md`.
4. Reclasser les gaps selon cette vue d'usage.
5. Mettre a jour le protocole pour maintenir ces buckets apres chaque PR significative.
6. Regenerer la vue Mermaid en groupes d'usage.

## 7_CANONICAL_STATE

| Produit | Etat produit porte | Vue usage rapide | NEXT_GO |
| --- | --- | --- | --- |
| ClickUp Cockpit | `USABLE_LIMITED` | `USABLE_LIMITED` | Besoin reel ou upgrade plan seulement |
| Repo KG | `USABLE_NOW` | `USABLE_NOW` | `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01` |
| Airtable Orchestration Layer | `DOC_ONLY_READY / GO_LIMITED` | `DOC_ONLY` | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| Botpress Adapter | `SIMULATED_PASS` | `SIMULATED_ONLY` | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |
| OpenClaw Docs Library | `DOC_ONLY_READY` | `DOC_ONLY` | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` |
| BTC COIN-M Accumulation Engine | `NOT_USABLE_YET / DO_NOT_USE_LIVE` | `FORBIDDEN_LIVE` | Validation du parent puis child formules dedie |

## 11_KEY_DECISIONS

- La vue usage est un overlay de lecture, pas un remplacement des statuts produit.
- Quand plusieurs statuts coexistent, la lecture operateur doit prendre le sens le plus prudent.
- `DOC_ONLY_READY / GO_LIMITED` se lit `DOC_ONLY` du point de vue usage actuel.
- `NOT_USABLE_YET / DO_NOT_USE_LIVE` se lit `FORBIDDEN_LIVE`.

## 12_INVARIANTS

- Aucun runtime modifie.
- Aucun secret.
- Aucun produit promu artificiellement.
- Aucun guide live ajoute pour Airtable ou BTC COIN-M.
- La preuve reste dans le repo, pas dans la vue rapide elle-meme.

## 17_RESUME_POINT

```text
docs/product/PRODUCT_USAGE_MATRIX.md
docs/product/PRODUCT_USAGE_ATLAS.md
docs/product/FINAL_TARGET_GAPS.md
docs/product/UPDATE_PROTOCOL.md
```

## RISKS

- À qualifier.
