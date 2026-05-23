# GO_OPT_TRADING_DOC_OPS_CANONIZE_BUNDLE_PATCH_ZIP_01

## Concept

Élever le standard bundle + .patch + .zip dans la matrice maîtresse doc-ops
et clarifier BUNDLE_TYPES.md avec le type "Patch transport bundle".

La chaîne canonique (combined → matrix → method → format) est livrée et prouvée
opérationnellement. La matrice maîtresse et la typologie des bundles doivent
maintenant l'absorber comme règle supérieure.

## Scope

- Modifier `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- Modifier `bundles/BUNDLE_TYPES.md`
- Créer `docs/chantiers/<GO_ID>/00_INITIAL_PROJECT_DOC.md`
- Créer `docs/index/inbox/<GO_ID>.md`

## Modifications

### Matrice — Partie 8.1

Ajouter la ligne : `bundle déportable / patch / archive de transport`

### Matrice — Partie 10.1.1 (nouvelle)

Ajouter le standard : `bundle + .patch + .zip` comme format canonique de transport.

### Matrice — Partie 11

Ajouter les interdits :
- `.patch` orphelin non archivé dans un bundle
- `.zip` souverain (le `.zip` ne remplace pas le bundle)
- bundle sans chantier ni inbox

### BUNDLE_TYPES.md

Ajouter le type `Patch transport bundle`.

## Invariants

- doc-only
- ne pas toucher runtime
- ne pas modifier les index globaux
- `.zip` = transport, pas source canonique
- `.patch` = artefact canonique Git
- bundle source = `bundles/<GO_ID>/`
- chantier source = `docs/chantiers/<GO_ID>/`
