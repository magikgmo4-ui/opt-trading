---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-18
topic_keys:
  - product_usage
  - atlas
  - rescan
  - delta_refresh
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01/90_CLOSEOUT.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# INBOX - GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01

## Objet

Rattraper les deltas produits posterieurs au `2026-05-07` sans rejouer l'inventaire repo complet.

## Resultat

**PASS** - Refresh doc-only applique :

- `Deepseek Student` ajoute a l'Atlas en `USABLE_LIMITED` ;
- `Bot Vision` et `derivatives_collector` synchronises sur des preuves plus recentes ;
- `PROJECT_PRESENTATION.md` remis en ligne avec l'Atlas courant.

## Point de reprise

```text
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01/90_CLOSEOUT.md
docs/product/PRODUCT_USAGE_MATRIX.md
docs/product/PRODUCT_USAGE_ATLAS.md
```

## RISKS

- À qualifier.
