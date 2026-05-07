---
doc_id: OPT_TRADING_PROJECT_PRESENTATION
doc_type: project_presentation
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/FINAL_TARGET_GAPS.md
---

# Project Presentation

## Ce que ce dossier apporte

Cette couche produit donne une lecture humaine et durable du setup `opt-trading` sans remplacer les preuves canoniques du repo.

Elle sert a repondre a trois questions simples :
1. Quelles surfaces existent vraiment ?
2. Qu'est-ce qui est utilisable maintenant ?
3. Qu'est-ce qui reste seulement documente, simule, ou interdit en live ?

## Source canonique

Le repo reste la source canonique :
- docs ;
- commits ;
- PR ;
- closeouts ;
- index.

Le Product Usage Atlas est une couche de lecture utilisateur.

## Lecture recommandee

1. `PRODUCT_USAGE_MATRIX.md` pour voir l'etat rapide.
2. `PRODUCT_USAGE_ATLAS.md` pour comprendre chaque produit.
3. `FINAL_TARGET_GAPS.md` pour voir ce qui manque.
4. `guides/` pour utiliser les surfaces deja bornees.

## Produits suivis maintenant

| Produit | Statut porte | Usage actuel |
| --- | --- | --- |
| ClickUp Cockpit | `USABLE_LIMITED` | Cockpit humain pour piloter les GO |
| Repo KG | `USABLE_NOW` | Projection repo-first utilisable tout de suite |
| Airtable Orchestration Layer | `DOC_ONLY_READY / GO_LIMITED` | Produit cadre, pas encore un runtime borne |
| Botpress Adapter | `SIMULATED_PASS` | Tests et smoke simules, pas de reel complet |
| OpenClaw Docs Library | `DOC_ONLY_READY` | Lecture et cartographie documentaire |
| BTC COIN-M Accumulation Engine | `NOT_USABLE_YET / DO_NOT_USE_LIVE` | Cadrage mathematique, aucun usage live |

## Ce qu'il ne faut pas conclure

- `PASS` chantier ne veut pas dire `PRODUCT_FINISHED`.
- Une app externe ne devient pas source de verite.
- Un produit simule n'est pas un produit live.
- Un produit documente n'est pas un produit utilisable.

## Documents de cette couche

```text
docs/product/PROJECT_PRESENTATION.md
docs/product/PRODUCT_USAGE_ATLAS.md
docs/product/PRODUCT_USAGE_MATRIX.md
docs/product/FINAL_TARGET_GAPS.md
docs/product/PRODUCT_USAGE_GRAPH.mmd
docs/product/UPDATE_PROTOCOL.md
docs/product/guides/
```
