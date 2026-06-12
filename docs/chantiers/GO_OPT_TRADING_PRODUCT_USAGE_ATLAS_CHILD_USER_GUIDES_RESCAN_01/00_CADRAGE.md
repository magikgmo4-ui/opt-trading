---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_RESCAN_01_CADRAGE
doc_type: cadrage
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_RESCAN_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: open
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01/90_CLOSEOUT.md
  - docs/product/guides/README.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# 00_CADRAGE - GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_RESCAN_01

## 1_MASTER_TARGET

Resynchroniser la couche `docs/product/guides/*` avec l'Atlas rescanne, sans surpromouvoir les produits ni modifier le runtime.

## 2_BASE_STATE

- `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01` = `PASS`.
- `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01` = `PASS`.
- L'Atlas suit maintenant 14 produits.
- `Deepseek Student` n'a pas encore de guide dans `docs/product/guides/`.
- Plusieurs entrees de `PRODUCT_USAGE_ATLAS.md` portent encore `user_guide: none_yet` alors que les guides existent deja.
- `Repo KG` pointe encore vers le child ferme `USER_GUIDES_01` dans certaines vues produit.

## 3_INITIAL_NEED

Le besoin n'est pas de rejouer `USER_GUIDES_01`, mais de fermer le delta ouvert par le rescan :

1. ajouter le guide `Deepseek Student` ;
2. rafraichir `Bot Vision` et `derivatives_collector` ;
3. remettre `PRODUCT_USAGE_ATLAS.md`, `PRODUCT_USAGE_MATRIX.md` et `guides/README.md` en coherence avec la couverture guide reelle ;
4. retirer les pointeurs produit qui envoient encore vers le child ferme `USER_GUIDES_01`.

## 4_MASTER_PROJECT_PLAN

1. Relire les guides existants et l'Atlas rescanne.
2. Ajouter le guide manquant.
3. Rafraichir les guides dont le `NEXT_GO` ou l'etat ont derive.
4. Rebrancher les chemins de guide dans `PRODUCT_USAGE_ATLAS.md`.
5. Rebrancher la lecture de couverture dans `PRODUCT_USAGE_MATRIX.md` et `guides/README.md`.
6. Retirer les pointeurs produit stale vers `USER_GUIDES_01`.
7. Fermer avec un closeout doc-only.

## 7_CANONICAL_STATE

| Etat | Valeur |
| --- | --- |
| Produits dans l'Atlas | 14 |
| Guides presents avant ce child | 13 |
| Guide manquant | `DEEPSEEK_STUDENT.md` |
| Guides a rafraichir | `BOT_VISION.md`, `DERIVATIVES_COLLECTOR.md` |
| References Atlas stale | Oui (`user_guide: none_yet` sur plusieurs entrees) |

## 11_KEY_DECISIONS

- Aucun nouveau guide live n'est cree pour une surface non validee.
- `Deepseek Student` recoit un guide `USABLE_LIMITED`, pas un guide de decision autonome.
- `Bot Vision` et `derivatives_collector` gardent leur bucket `USABLE_LIMITED`.
- Les guides doc-only et la notice BTC existantes sont seulement rebranches dans l'Atlas, pas reecrits.

## 12_INVARIANTS

- Doc-only uniquement.
- Aucun runtime modifie.
- Aucun secret.
- Aucun bucket nouveau.
- Aucun langage de promotion implicite.

## 16_TODO

1. Creer `01_GUIDE_DELTA_PLAN.md`.
2. Creer `02_GUIDE_COVERAGE_MATRIX.md`.
3. Creer `docs/product/guides/DEEPSEEK_STUDENT.md`.
4. Mettre a jour `docs/product/guides/BOT_VISION.md`.
5. Mettre a jour `docs/product/guides/DERIVATIVES_COLLECTOR.md`.
6. Mettre a jour `docs/product/guides/README.md`.
7. Mettre a jour `docs/product/PRODUCT_USAGE_ATLAS.md`.
8. Mettre a jour `docs/product/PRODUCT_USAGE_MATRIX.md`.
9. Creer `90_CLOSEOUT.md` et l'entree inbox.

## 17_RESUME_POINT

```text
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_RESCAN_01/01_GUIDE_DELTA_PLAN.md
docs/product/guides/README.md
```

## RISKS

- À qualifier.
