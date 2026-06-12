---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01_USAGE_VIEW
doc_type: usage_view
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
---

# 01_USAGE_VIEW - Vue usage produit

## Buckets autorises

```text
USABLE_NOW
USABLE_LIMITED
DOC_ONLY
SIMULATED_ONLY
FORBIDDEN_LIVE
```

## Mapping depuis les statuts produit

| Statut produit porte | Vue usage rapide |
| --- | --- |
| `USABLE_NOW` | `USABLE_NOW` |
| `USABLE_LIMITED` | `USABLE_LIMITED` |
| `DOC_ONLY_READY` | `DOC_ONLY` |
| `DOC_ONLY_READY / GO_LIMITED` | `DOC_ONLY` |
| `SIMULATED_PASS` | `SIMULATED_ONLY` |
| `NOT_USABLE_YET / DO_NOT_USE_LIVE` | `FORBIDDEN_LIVE` |

## Precedence prudente

Si plusieurs signaux coexistent, garder la lecture la plus prudente :

```text
FORBIDDEN_LIVE
> SIMULATED_ONLY
> DOC_ONLY
> USABLE_LIMITED
> USABLE_NOW
```

## Application courante

| Bucket | Produits | Lecture operateur |
| --- | --- | --- |
| `USABLE_NOW` | Repo KG | Utilisable maintenant comme projection repo-first read-only. |
| `USABLE_LIMITED` | ClickUp Cockpit | Utilisable maintenant pour piloter, avec limites plan gratuit connues. |
| `DOC_ONLY` | Airtable Orchestration Layer, OpenClaw Docs Library | Lecture et cadrage seulement ; ne pas presenter ces surfaces comme produits runtime finis. |
| `SIMULATED_ONLY` | Botpress Adapter | Simulation et smoke seulement ; pas de lecture live-ready. |
| `FORBIDDEN_LIVE` | BTC COIN-M Accumulation Engine | Aucun usage live ou runtime autorise a ce stade. |

## Acceptance locale

La vue usage est valide si :
- tous les produits du socle initial sont ranges dans un bucket clair ;
- chaque bucket porte une lecture operateur simple ;
- aucun produit non valide n'est promu artificiellement.

## RISKS

- À qualifier.
