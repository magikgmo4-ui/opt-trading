---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01_ATLAS_PATCH
doc_type: patch_plan
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/product/PROJECT_PRESENTATION.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/product/PRODUCT_USAGE_GRAPH.mmd
---

# 02_ATLAS_PATCH - Patch applique

## Surface ajoutee

| Surface | Bucket | Justification resumee |
| --- | --- | --- |
| Deepseek Student | `USABLE_LIMITED` | Runbook operateur, wrappers documentes, workspace canonique clarifie, mais legacy conserve et integration large encore bornee |

## Surfaces rafraichies

| Surface | Type de refresh | Resultat |
| --- | --- | --- |
| Bot Vision | preuves, gap, `NEXT_GO` | entree synchronisee sur `VISION_RUNTIME_CONSOLIDATION_IMPL_01` |
| derivatives_collector | preuves, gap, `NEXT_GO` | entree synchronisee sur la chaine collectors jusqu'a la decision selective d'extraction |
| Project Presentation | couverture | presentation alignee sur les produits vraiment suivis par l'Atlas |

## Fichiers patches

| Fichier | Patch |
| --- | --- |
| `docs/product/PROJECT_PRESENTATION.md` | table des surfaces suivies alignee sur l'Atlas courant |
| `docs/product/PRODUCT_USAGE_MATRIX.md` | +1 entree produit, refresh de 2 entrees existantes |
| `docs/product/PRODUCT_USAGE_ATLAS.md` | +1 fiche produit, refresh de 2 fiches existantes |
| `docs/product/FINAL_TARGET_GAPS.md` | +1 gap produit, refresh de 2 gaps existants |
| `docs/product/PRODUCT_USAGE_GRAPH.mmd` | noeud `Deepseek Student` + edges `NEXT_GO` mis a jour |

## Hors scope garde

- `PERF` reste hors Atlas.
- Aucun guide utilisateur nouveau n'est cree.
- Aucun runtime n'est modifie.
