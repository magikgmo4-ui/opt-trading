---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01_CADRAGE
doc_type: cadrage
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: open
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/03_ATLAS_UPDATE_PROPOSAL.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/product/PRODUCT_USAGE_GRAPH.mmd
  - docs/product/UPDATE_PROTOCOL.md
---

# 00_CADRAGE - GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01

## 1_MASTER_TARGET

Appliquer dans `docs/product/*` les sept surfaces `ADD_TO_ATLAS` validees par l'inventaire repo, sans promouvoir les surfaces `KEEP_CANDIDATE`, `DO_NOT_PROMOTE`, `ARCHIVE_ONLY`, `A AUDITER` ou `UNKNOWN`.

## 2_INITIAL_PROJECT_DOC

Ce fichier ouvre le child d'application de l'inventaire repo dans la couche Product Usage Atlas.

Le child precedent `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01` a produit l'inventaire, les propositions et le classement. Ce nouveau child applique uniquement les entrees validees pour l'Atlas.

## 3_INITIAL_NEED

La PR #240 a merge l'inventaire repo et a corrige le NEXT_GO vers ce child d'application. Le besoin courant est de materialiser dans les fichiers `docs/product/*` les entrees `ADD_TO_ATLAS` deja proposees et sourcees.

## 4_MASTER_PROJECT_PLAN

1. Relire la closeout et la proposition d'ajout a l'Atlas.
2. Appliquer les sept entrees `ADD_TO_ATLAS` dans `PRODUCT_USAGE_MATRIX.md` et `PRODUCT_USAGE_ATLAS.md`.
3. Ajouter les gaps correspondants dans `FINAL_TARGET_GAPS.md`.
4. Mettre a jour `PRODUCT_USAGE_GRAPH.mmd`.
5. Mettre a jour `UPDATE_PROTOCOL.md` seulement si necessaire.
6. Ne pas creer de guide utilisateur live dans ce child.
7. Ne pas promouvoir les candidats non prouves.

## 6_FINAL_TARGET

Produire une couche produit ou les surfaces suivantes sont effectivement visibles dans `docs/product/*` :

| Surface | Bucket attendu |
| --- | --- |
| Desk Pro | `USABLE_LIMITED` |
| Bot Vision | `USABLE_LIMITED` |
| TradingView / Telegram Alert Pipeline | `USABLE_LIMITED` |
| OpenClaw Runtime | `USABLE_LIMITED` |
| derivatives_collector | `USABLE_LIMITED` |
| Trading Dual Stack V1 / XAUUSD | `DOC_ONLY` |
| LocalCMS | `DOC_ONLY` |

## 7_CANONICAL_STATE

- Product Usage Atlas parent merge : PR #237, merge `570a2dd`.
- Usage View child merge : PR #238, merge `8425078`.
- Repo Inventory child merge : PR #240, merge `161ddd3`.
- Les sept entrees `ADD_TO_ATLAS` sont proposees mais pas encore appliquees dans `docs/product/*`.
- L'arbre hypothetique reste une aide de priorisation et ne remplace pas `PRODUCT_USAGE_MATRIX.md`.

## 8_VALIDATED_PLAN

Plan valide : appliquer strictement les sept ajouts sourcees, puis fermer avec un closeout PASS/PASS_LIMITED. Les guides utilisateur sont une etape ulterieure.

## 11_KEY_DECISIONS

- `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01` prime maintenant sur `USER_GUIDES` comme next step immediat.
- `USER_GUIDES` reste ulterieur.
- `03_ATLAS_UPDATE_PROPOSAL.md` est la source de proposition.
- `04_SYNTHESIS_AND_HYPOTHETICAL_TREE.md` est une aide de priorisation, non source souveraine.
- Aucune entree `KEEP_CANDIDATE` ne doit etre appliquee a l'Atlas dans ce child.

## 12_INVARIANTS

- Repo = source canonique.
- Product Usage Atlas = lecture utilisateur.
- Aucun runtime modifie.
- Aucun secret.
- Aucun guide live nouveau.
- Aucun nouveau bucket.
- Aucun produit non prouve presente comme fini.
- Ne pas changer le statut prudent de BTC COIN-M, Airtable ou Botpress.

## 13_ESTABLISHED

- PR #240 est mergee.
- L'inventaire repo est disponible.
- Les sept ajouts `ADD_TO_ATLAS` sont clairement identifies.
- Le child courant doit appliquer, pas reinventer l'inventaire.

## 14_HYPOTHESIS

- Certains ajouts pourront rester `PASS_LIMITED` si les sources canoniques necessaires sont insuffisantes pour une entree detaillee complete.

## 15_REMAINING_GAP

- Les sept entrees ne sont pas encore visibles dans `PRODUCT_USAGE_MATRIX.md` et `PRODUCT_USAGE_ATLAS.md`.
- Les gaps correspondants ne sont pas encore materialises dans `FINAL_TARGET_GAPS.md`.
- Le graphe produit ne contient pas encore ces nouvelles surfaces.

## 16_TODO

1. Creer `01_APPLY_PLAN.md`.
2. Mettre a jour `docs/product/PRODUCT_USAGE_MATRIX.md`.
3. Mettre a jour `docs/product/PRODUCT_USAGE_ATLAS.md`.
4. Mettre a jour `docs/product/FINAL_TARGET_GAPS.md`.
5. Mettre a jour `docs/product/PRODUCT_USAGE_GRAPH.mmd`.
6. Creer `90_CLOSEOUT.md`.
7. Creer l'entree `docs/index/inbox/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01.md`.

## 17_RESUME_POINT

Reprendre depuis :

```text
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/03_ATLAS_UPDATE_PROPOSAL.md
```

Puis appliquer uniquement les sept entrees `ADD_TO_ATLAS` dans :

```text
docs/product/PRODUCT_USAGE_MATRIX.md
docs/product/PRODUCT_USAGE_ATLAS.md
docs/product/FINAL_TARGET_GAPS.md
docs/product/PRODUCT_USAGE_GRAPH.mmd
```

## RISKS

- À qualifier.
