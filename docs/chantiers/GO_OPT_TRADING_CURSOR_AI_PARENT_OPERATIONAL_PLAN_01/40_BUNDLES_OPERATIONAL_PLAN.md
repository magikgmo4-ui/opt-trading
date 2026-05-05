---
doc_id: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01_40_BUNDLES_PLAN
doc_type: chantier/bundles_plan
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 40_BUNDLES_OPERATIONAL_PLAN

## Statut Bundles

- **Statut** : `APPLICATION_DOCUMENTED_NOT_PRODUCT_CLOSED`
- **PR mergee** : PR #202 (`go/GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_IMPL_01`)
- **Doc parent** : `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` (MERGE)
- **Branche appliquee** : mergee, branche supprimee

## Role dans le workflow cursor-ai

Bundles est le mecanisme de packaging documentaire du repo opt-trading. Il structure :
- les lots documentaires par chantier ;
- le rattachement aux GO parents ;
- la conservation des paquets post-merge.

## Produit non ferme

- L'application Bundles est documentee comme workflow.
- Le produit Bundles n'est pas marque comme ferme.
- La reprise Bundles (`GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01`) reste possible comme GO candidat.

## Prochains usages Bundles

1. Packaging des Claude artifacts comme lot documentaire.
2. Packaging du plan parent cursor-ai.
3. Generation de la fiche de reprise operateur.

## Lien avec Claude artifacts

Le pack Claude artifacts (`GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01`) utilisera Bundles pour structurer ses livrables.
