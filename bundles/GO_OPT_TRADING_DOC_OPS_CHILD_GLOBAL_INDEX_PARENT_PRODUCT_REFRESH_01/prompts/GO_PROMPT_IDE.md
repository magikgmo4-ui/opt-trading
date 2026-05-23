# GO_PROMPT_IDE — GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01

Tu travailles dans le repo `opt-trading`.

## GO

`GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01`

## Target

`TARGET_GLOBAL_INDEX_PARENT_PRODUCT_ONLY_01`

## Master target

`MASTER_TARGET_CONTINUITY_INDEX_CLEAN_PARENT_PRODUCT_STATE_01`

## Mission

Mettre à jour les index globaux pour qu'ils reflètent l'état actuel uniquement au niveau des chantiers parents avec produit fini utilisable ou produit cible utilisable.

## Préchecks obligatoires

```bash
git status --short
git branch --show-current
git fetch --prune origin
git log --oneline --decorate -5
git diff --stat
```

Si la branche courante n'est pas dédiée, créer :

```bash
git switch -c go/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01
```

ou, si la branche existe déjà :

```bash
git switch go/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01
git rebase origin/sot/mainline
```

## Lire avant modification

```text
docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
docs/index/GO_INDEX.md
docs/index/ACTIVE_STREAMS.md
docs/index/NEXT_GO_CANDIDATES.md
docs/index/REPRISE.md
docs/index/GO_CLOSED_INDEX.md
bundles/BUNDLE_TARGET_INDEX.md
```

## Règle centrale

Les index globaux doivent contenir seulement :

```text
PARENT + PRODUIT UTILISABLE + STATUT + TARGET + NEXT ACTION
```

Retirer des index globaux actifs :

```text
enfants techniques
micro-GO
bundles
patchs
branches
PR
références historiques
artefacts support
```

## Scope de modification

Autorisé :

```text
docs/index/GO_INDEX.md
docs/index/ACTIVE_STREAMS.md
docs/index/NEXT_GO_CANDIDATES.md
docs/index/REPRISE.md
docs/index/GO_CLOSED_INDEX.md
bundles/BUNDLE_TARGET_INDEX.md si nécessaire
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/00_INITIAL_PROJECT_DOC.md
docs/index/inbox/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01.md
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/...
```

Interdit :

```text
runtime
cleanup branches
scripts runtime
modules runtime
secrets
modification de BRANCH_STATE.md sauf note stale/recount strictement nécessaire
```

## Sorties attendues

1. Classification des entrées existantes :
   - `KEEP_PARENT_PRODUCT`
   - `MOVE_TO_CLOSED`
   - `KEEP_LOCAL_ONLY`
   - `MOVE_TO_INBOX`
   - `DROP_FROM_GLOBAL_INDEX`
   - `NEEDS_REVIEW`

2. Index réécrits en parent-product-only.

3. Bundle transport mis à jour :

```text
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/README_BUNDLE.md
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/TARGETS.md
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/bundle_meta/target_card.json
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/patches/README_PATCHES.md
```

4. Patch canonique archivé :

```text
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/patches/<YYYYMMDD>_GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01_global_index_parent_product_refresh.patch
```

5. Aucun `.patch` racine committé.

## Validation

```bash
git diff --check
git status --short
git diff --stat
```

Puis ouvrir une PR doc-only.
