# PR BODY — modèle

## Summary

Met à jour les index globaux pour qu'ils reflètent l'état actuel uniquement au niveau des chantiers parents avec produit fini utilisable ou produit cible utilisable.

## Target

`TARGET_GLOBAL_INDEX_PARENT_PRODUCT_ONLY_01`

## Master target

`MASTER_TARGET_CONTINUITY_INDEX_CLEAN_PARENT_PRODUCT_STATE_01`

## Modifications

- `GO_INDEX.md` : parent-product-only
- `ACTIVE_STREAMS.md` : parents vivants uniquement
- `NEXT_GO_CANDIDATES.md` : 1 parent -> 1 target / next GO
- `REPRISE.md` : reprise courte et opératoire
- `GO_CLOSED_INDEX.md` : déplacements CLOSED/PASS si nécessaire
- `BUNDLE_TARGET_INDEX.md` : refresh bundle/target si nécessaire

## Invariants

- Doc-only.
- Aucun runtime.
- Aucun cleanup branches.
- Aucun `.patch` racine committé.
- Enfants/micro-GO conservés hors index globaux actifs.

## Validation

- [ ] `git diff --check`
- [ ] `git status --short`
- [ ] Relecture des index
- [ ] PR doc-only
