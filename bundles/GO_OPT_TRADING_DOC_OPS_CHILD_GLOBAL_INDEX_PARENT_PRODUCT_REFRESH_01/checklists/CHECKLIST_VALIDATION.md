# CHECKLIST_VALIDATION — GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01

## Préconditions

- [ ] `git fetch --prune origin` exécuté.
- [ ] Branche dédiée utilisée : `go/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01`.
- [ ] Matrice relue.
- [ ] PR #705 présente dans `sot/mainline`.

## Classification

- [ ] Chaque entrée de `GO_INDEX.md` classée.
- [ ] Chaque flux de `ACTIVE_STREAMS.md` classé.
- [ ] Chaque next GO de `NEXT_GO_CANDIDATES.md` classé.
- [ ] Chaque point de reprise de `REPRISE.md` classé.
- [ ] Entrées CLOSED/PASS vérifiées contre `GO_CLOSED_INDEX.md`.

## Réécriture

- [ ] `GO_INDEX.md` ne contient que des parents produits.
- [ ] `ACTIVE_STREAMS.md` ne contient que des parents vivants.
- [ ] `NEXT_GO_CANDIDATES.md` respecte 1 parent -> 1 target/next GO.
- [ ] `REPRISE.md` est court et opératoire.
- [ ] Les enfants/micro-GO sont retirés du global actif.
- [ ] Les détails sont conservés dans chantier/inbox/bundle/closed.

## Transport

- [ ] `bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/` existe.
- [ ] `TARGETS.md` existe.
- [ ] `bundle_meta/target_card.json` existe.
- [ ] `patches/README_PATCHES.md` existe.
- [ ] Patch final archivé sous `bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/patches/`.
- [ ] Aucun `.patch` racine committé.
- [ ] `.zip` éventuel considéré comme transport, pas source canonique.

## Validation Git

- [ ] `git diff --check` PASS.
- [ ] `git status --short` vérifié.
- [ ] Aucun runtime modifié.
- [ ] Aucun cleanup branch fait.
- [ ] PR doc-only ouverte.
