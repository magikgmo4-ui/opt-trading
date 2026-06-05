---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-07
topic_keys:
  - product_usage
  - apply_inventory
  - atlas
  - add_to_atlas
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01/90_CLOSEOUT.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# INBOX - GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01

## Objet

Appliquer strictement les 7 entrees `ADD_TO_ATLAS` validees par l'inventaire repo dans `docs/product/*`.

## Resultat

**PASS** - 7 nouvelles entrees materialisees dans la matrice, l'atlas, les gaps et le graphe. Atlas passe de 6 a 13 produits.

| Bucket | Nb avant | Nb apres |
| --- | --- | --- |
| `USABLE_NOW` | 1 | 1 |
| `USABLE_LIMITED` | 1 | 7 |
| `DOC_ONLY` | 2 | 4 |
| `SIMULATED_ONLY` | 1 | 1 |
| `FORBIDDEN_LIVE` | 1 | 1 |

Aucun runtime modifie. Aucun secret.

## Point de reprise

```text
docs/product/PRODUCT_USAGE_MATRIX.md
docs/product/PRODUCT_USAGE_ATLAS.md
```

## RISKS

- À qualifier.
