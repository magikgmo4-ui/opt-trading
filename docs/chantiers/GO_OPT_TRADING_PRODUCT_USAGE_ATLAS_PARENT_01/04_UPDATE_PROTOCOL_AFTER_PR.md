---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01_UPDATE_PROTOCOL_AFTER_PR
doc_type: protocol
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
---

# 04_UPDATE_PROTOCOL_AFTER_PR - Mise a jour apres PR significative

## Regle centrale

Apres chaque PR significative qui change un produit, un closeout, une capacite d'usage, un gap ou un guide :

1. Lire le closeout, le diff et les preuves repo.
2. Identifier les produits touches.
3. Mettre a jour `docs/product/PRODUCT_USAGE_MATRIX.md`.
4. Mettre a jour `docs/product/PRODUCT_USAGE_ATLAS.md` si le mode d'usage ou la lecture du produit change.
5. Mettre a jour le guide associe si l'usage autorise change.
6. Mettre a jour `docs/product/FINAL_TARGET_GAPS.md`.
7. Regenerer `docs/product/PRODUCT_USAGE_GRAPH.mmd` si les relations ou statuts changent.
8. Verifier qu'aucun produit non valide n'a ete promu par glissement de langage.

## Promotions interdites sans preuve

- `DOC_ONLY_READY` -> `USABLE_NOW`
- `SIMULATED_PASS` -> `PRODUCT_FINISHED`
- `NOT_USABLE_YET` -> `USABLE_LIMITED`

## Sorties minimales a toucher

```text
docs/product/PRODUCT_USAGE_MATRIX.md
docs/product/PRODUCT_USAGE_ATLAS.md
docs/product/FINAL_TARGET_GAPS.md
docs/product/UPDATE_PROTOCOL.md
```

## RISKS

- À qualifier.
