# GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_BUNDLE_01

## Concept

Reconditionner le patch source `CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01` comme bundle
doc-ops autonome compatible target/master_target, sans application directe du patch
original. Le bundle formalise le format d'exécution des patchs zip comme processus
documenté, avec job packets AI workers, sans toucher au runtime ni aux index globaux.

## Source

Le patch source `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch`
contient 18 fichiers : 1 governance doc, 8 chantier docs, 1 inbox entry, 8 job packets.
Il est conservé sous `bundles/<GO_ID>/patches/` comme artefact source.

## Règles

- doc-only
- ne pas appliquer le patch original directement
- ne pas toucher runtime
- ne pas toucher index globaux
- ne pas committer de .patch à la racine
- ajouter TARGETS.md + target_card.json

## Fichiers

```
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_BUNDLE_01/00_INITIAL_PROJECT_DOC.md
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_BUNDLE_01/README_BUNDLE.md
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_BUNDLE_01/TARGETS.md
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_BUNDLE_01/bundle_meta/target_card.json
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_BUNDLE_01/patches/README_PATCHES.md
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_BUNDLE_01/patches/<dated>_<GO_ID>_source_child_patch_zip_execution_format_v2_01.patch
docs/index/inbox/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_BUNDLE_01.md
```
