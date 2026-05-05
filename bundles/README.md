# Bundles — opt-trading

## Objet

Index des bundles disponibles dans le repo `opt-trading`. Les bundles sont des packs documentaires autonomes pour l'execution controlee de chantiers via IDE.

## Methode

Voir : `docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/`

## Bundles disponibles

| Bundle | Machine | Statut | Lien |
|---|---|---|---|
| `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01` | student | REFERENCE | [README](./GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/README_BUNDLE.md) |
| `GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01` | cursor-ai | REFERENCE | [docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/](../docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/) |
| `claude-artifacts` | cursor-ai | ACTIVE | [README](./claude-artifacts/README.md) |
| `CURSOR_AI_OPERATOR_REPRISE_PACKET` | cursor-ai | ACTIVE | [CURSOR_AI_OPERATOR_REPRISE_PACKET.md](./CURSOR_AI_OPERATOR_REPRISE_PACKET.md) |
| `ACTIVE_WORKFLOW` | cursor-ai | ACTIVE | [ACTIVE_WORKFLOW.md](./ACTIVE_WORKFLOW.md) |
| `BUNDLE_TYPES` | cursor-ai | ACTIVE | [BUNDLE_TYPES.md](./BUNDLE_TYPES.md) |
| `OPERATOR_FLOW` | cursor-ai | ACTIVE | [OPERATOR_FLOW.md](./OPERATOR_FLOW.md) |
| `NO_RUNTIME_NO_SENSITIVE_RULES` | cursor-ai | ACTIVE | [NO_RUNTIME_NO_SENSITIVE_RULES.md](./NO_RUNTIME_NO_SENSITIVE_RULES.md) |

## Conventions

- Un bundle = un dossier sous `bundles/` ou `docs/chantiers/`
- Contient au minimum : `README_BUNDLE.md`, `bundle_meta/manifest.json`
- Aucun secret, .env, token
- Doc-only ou scripts d'application sans runtime live
