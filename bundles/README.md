# Bundles — opt-trading

## Objet

Index des bundles disponibles dans le repo `opt-trading`. Les bundles sont des packs documentaires autonomes pour l'execution controlee de chantiers via IDE.

## Methode

Voir : `docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/`

## Bundles disponibles

| Bundle | Machine | Statut | Lien |
|---|---|---|---|
| `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01` | student | REFERENCE | [README](./GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/README_BUNDLE.md) |
| `GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01` | cursor-ai | ACTIVE | [docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/](../docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/) |

## Conventions

- Un bundle = un dossier sous `bundles/` ou `docs/chantiers/`
- Contient au minimum : `README_BUNDLE.md`, `bundle_meta/manifest.json`
- Aucun secret, .env, token
- Doc-only ou scripts d'application sans runtime live
