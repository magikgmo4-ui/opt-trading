---
doc_id: OPT_TRADING_PRODUCT_UPDATE_PROTOCOL
doc_type: update_protocol
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/04_UPDATE_PROTOCOL_AFTER_PR.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/01_USAGE_VIEW.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/02_NEXT_GO_BY_PRODUCT.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# Update Protocol

## Quand mettre a jour cette couche

Mettre a jour cette couche apres toute PR significative qui :
- change le mode d'usage d'un produit ;
- ferme un gap ;
- ouvre un nouveau gap ;
- fournit un closeout de preuve ;
- ajoute ou retire un guide ;
- change un interdit live.

## Procedure canonique

1. Lire le closeout, le diff et les preuves repo.
2. Identifier les produits touches.
3. Recalculer la `usage_view` de chaque produit touche avec la precedence prudente.
4. Mettre a jour la lecture rapide et la matrice detaillee dans `PRODUCT_USAGE_MATRIX.md`.
5. Mettre a jour `PRODUCT_USAGE_ATLAS.md`.
6. Mettre a jour le guide associe si l'usage autorise change.
7. Mettre a jour `FINAL_TARGET_GAPS.md`.
8. Mettre a jour `PRODUCT_USAGE_GRAPH.mmd` si la carte change.
9. Verifier que le langage ne surevalue pas le produit.

## Precedence prudente de lecture

```text
FORBIDDEN_LIVE
> SIMULATED_ONLY
> DOC_ONLY
> USABLE_LIMITED
> USABLE_NOW
```

## Buckets a maintenir

- `USABLE_NOW`
- `USABLE_LIMITED`
- `DOC_ONLY`
- `SIMULATED_ONLY`
- `FORBIDDEN_LIVE`

## Questions de controle

Avant de sauvegarder la mise a jour, verifier :
- Est-ce que PASS chantier est en train d'etre confondu avec produit fini ?
- Est-ce qu'une app externe est en train d'etre promue au rang de source canonique ?
- Est-ce qu'un guide live a ete ajoute pour une surface non validee ?
- Est-ce que la `usage_view` retenue est bien la lecture la plus prudente ?
- Est-ce que chaque gap pointe encore vers un NEXT_GO ?

## Promotions interdites sans preuve supplementaire

- `DOC_ONLY_READY` -> `USABLE_NOW`
- `SIMULATED_PASS` -> `PRODUCT_FINISHED`
- `NOT_USABLE_YET` -> `USABLE_LIMITED`

## Point de reprise

```text
docs/product/PRODUCT_USAGE_MATRIX.md
```
