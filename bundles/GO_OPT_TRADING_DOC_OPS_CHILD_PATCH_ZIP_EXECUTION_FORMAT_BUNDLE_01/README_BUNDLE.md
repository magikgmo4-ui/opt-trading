# Bundle — GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_BUNDLE_01

## Description

Bundle doc-ops autonome formalisant le format d'exécution des patchs zip
(processus de création, transport et application de patchs entre session
conversationnelle et IDE). Compatible target/master_target et matrice IDE.

## Contenu

| Chemin | Rôle |
|---|---|
| `TARGETS.md` | Définition target + master_target |
| `bundle_meta/target_card.json` | Fiche machine-readable du target |
| `patches/` | Patchs source archivés (dont le patch originel V2) |

## Dépendances

- `MASTER_TARGET_SESSION_TO_IDE_PATCH_TRANSPORT_01` — master target commun
- `GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01` — bundle matrice IDE
