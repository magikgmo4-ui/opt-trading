---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-07
topic_keys:
  - product_usage
  - repo_inventory
  - atlas
  - product_candidates
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/03_ATLAS_UPDATE_PROPOSAL.md
---

# INBOX - GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01

## Objet

Etendre l'inventaire du Product Usage Atlas au-dela des 6 produits du socle initial en scannant le repo pour identifier, classer et proposer les surfaces produit a ajouter.

## Resultat

**PASS** - 18 surfaces candidates inventoriees et classees :

| Decision | Surfaces |
| --- | --- |
| `ADD_TO_ATLAS` (7) | Desk Pro, Bot Vision, Trading Dual Stack V1, TradingView/Telegram Alert Pipeline, OpenClaw Runtime, LocalCMS, derivatives_collector |
| `KEEP_CANDIDATE` (7) | derivatives_analyzer, probability_engine, risk_engine, Deepseek Student, Collectors spot, Simex Bitget Bridge, validated_prompt_factory |
| `DO_NOT_PROMOTE` (4) | Git Fleet Guard, module_contextuals_shell, Ops wrappers, surfaces historiques |

Aucun runtime modifie. Aucun secret.

## Point de reprise

```text
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/03_ATLAS_UPDATE_PROPOSAL.md
```

## RISKS

- À qualifier.
