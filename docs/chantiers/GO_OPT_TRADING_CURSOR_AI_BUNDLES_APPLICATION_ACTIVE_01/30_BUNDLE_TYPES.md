---
doc_id: GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01_30_BUNDLE_TYPES
doc_type: chantier/bundle_types
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/BUNDLE_TYPES.md
---

# 30_BUNDLE_TYPES — Types de bundles utilisables cursor-ai

Les types de bundles sont definis dans `bundles/BUNDLE_TYPES.md`.

## Liste

| Type | Machine | Statut | Exemple |
| --- | --- | --- | --- |
| Reprise bundle | cursor-ai | ACTIF | `bundles/CURSOR_AI_BUNDLES_REPRISE.md` |
| Operator pack | cursor-ai | ACTIF | `bundles/claude-artifacts/` |
| IDE handoff bundle | cursor-ai | ACTIF | `docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/` |
| Prompt bundle | cursor-ai | ACTIF | `bundles/claude-artifacts/PROMPT_TEMPLATES.md` |
| PR merge bundle | cursor-ai | ACTIF | Template PR standard |
| Closeout bundle | cursor-ai | ACTIF | Template CLOSEOUT |
| Admin-trading gate bundle | admin-trading | FERME (futur) | Non ouvert |

## Regle d'extension

De nouveaux types de bundle peuvent etre ajoutes si :
1. Doc-only.
2. Pas de runtime.
3. Pas de secrets.
4. Documentes dans `bundles/BUNDLE_TYPES.md`.

## Mapping bundle existant → type

| Bundle existant | Type |
| --- | --- |
| `bundles/claude-artifacts/` | Operator pack |
| `bundles/CURSOR_AI_BUNDLES_REPRISE.md` | Reprise bundle |
| `bundles/ACTIVE_WORKFLOW.md` | Operator pack (ce GO) |
| `bundles/BUNDLE_TYPES.md` | Operator pack (ce GO) |
| `bundles/OPERATOR_FLOW.md` | Operator pack (ce GO) |
| `bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md` | Operator pack (ce GO) |
| `docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/` | IDE handoff bundle |
