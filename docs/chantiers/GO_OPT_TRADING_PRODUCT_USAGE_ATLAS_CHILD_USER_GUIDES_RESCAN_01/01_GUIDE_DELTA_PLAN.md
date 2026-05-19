---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_RESCAN_01_GUIDE_DELTA_PLAN
doc_type: guide_plan
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_RESCAN_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/product/guides/BOT_VISION.md
  - docs/product/guides/DERIVATIVES_COLLECTOR.md
  - docs/product/guides/DEEPSEEK_STUDENT.md
---

# 01_GUIDE_DELTA_PLAN - Delta guide

## Changements prevus

| Surface | Action | Pourquoi |
| --- | --- | --- |
| Deepseek Student | CREATE | Le produit a ete ajoute a l'Atlas par le rescan, mais la couche guides ne couvre encore que 13 produits. |
| Bot Vision | REFRESH | Le guide pointe encore vers `VISION_FAMILY_SURVIVOR_DECISION` au lieu de la stabilisation runtime plus recente. |
| derivatives_collector | REFRESH | Le guide pointe encore vers `GO_COLLECTORS_BASELINE_INVENTORY_01` alors que la chaine doctrine/extraction a avance. |
| guides/README.md | REFRESH | Le guide index doit passer de 13 a 14 guides et prendre en compte le delta. |
| PRODUCT_USAGE_ATLAS.md | REFRESH | Les champs `user_guide` doivent pointer vers les vrais guides deja presents. |
| PRODUCT_USAGE_MATRIX.md | REFRESH | La colonne "Guide utilisateur requis ?" doit cesser de signaler des faux `none_yet`. |
| FINAL_TARGET_GAPS.md / PRODUCT_USAGE_GRAPH.mmd | REFRESH | `Repo KG` ne doit plus pointer vers le child ferme `USER_GUIDES_01` comme prochaine action. |

## Hors scope

- Reecrire les guides doc-only existants.
- Promouvoir `Deepseek Student` au-dessus de `USABLE_LIMITED`.
- Changer la taxonomie produit.
