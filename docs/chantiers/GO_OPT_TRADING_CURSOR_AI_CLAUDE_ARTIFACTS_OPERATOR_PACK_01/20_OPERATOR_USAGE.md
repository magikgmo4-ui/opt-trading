---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_20_OPERATOR_USAGE
doc_type: chantier/operator_usage
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/claude-artifacts/README.md
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
  - bundles/claude-artifacts/REPRISE_TEMPLATE.md
  - bundles/claude-artifacts/NO_COMMIT_RULES.md
---

# 20_OPERATOR_USAGE

Guide d'usage du pack operateur Claude artifacts pour cursor-ai.

## Quand utiliser Claude artifacts

- Pour standardiser la reprise d'un GO (prompt de reprise).
- Pour standardiser la review d'un GO avant merge (prompt de review).
- Pour standardiser le merge d'un GO doc-only (prompt de merge).
- Pour verifier l'absence de runtime dans un GO (safety check).
- Pour produire un handoff IDE lisible (prompt de handoff).
- Pour creer une fiche de reprise standard (reprise template).

## Quand utiliser Bundles

- Pour structurer les livrables documentaires d'un GO.
- Pour packager les artefacts reutilisables (prompts, templates, regles).
- Pour indexer les bundles disponibles.

## Quand NE PAS utiliser le pack

- **Ne pas utiliser** pour modifier du runtime.
- **Ne pas utiliser** pour toucher admin-trading sans demande explicite.
- **Ne pas utiliser** pour modifier `systemd`, le webhook serveur, ou le risk engine.
- **Ne pas utiliser** pour committer des secrets, .env, tokens.
- **Ne pas utiliser** pour marquer `alert_webhook` comme ferme.
- **Ne pas utiliser** pour marquer `Bundles produit` comme ferme.

## Workflow standard

1. **Reprise** : utiliser `PROMPT_TEMPLATES.md` > Template 1 (reprise)
2. **Creation** : creer les fichiers GO selon la spec
3. **Safety check** : utiliser `PROMPT_TEMPLATES.md` > Template 4 (no-runtime)
4. **Review** : utiliser `PROMPT_TEMPLATES.md` > Template 2 (review)
5. **Merge** : utiliser `PROMPT_TEMPLATES.md` > Template 3 (merge doc-only)
6. **Handoff** : utiliser `PROMPT_TEMPLATES.md` > Template 5 (handoff IDE)
7. **Reprise fiche** : utiliser `REPRISE_TEMPLATE.md`

## Regles de lecture

- `bundles/claude-artifacts/README.md` : survol et index du pack.
- `bundles/claude-artifacts/PROMPT_TEMPLATES.md` : templates de prompts.
- `bundles/claude-artifacts/REPRISE_TEMPLATE.md` : template de fiche de reprise.
- `bundles/claude-artifacts/NO_COMMIT_RULES.md` : regles de non-commit.

## Extensions futures

Le pack peut etre etendu avec :
- `bundles/claude-artifacts/CHECKLIST_EXECUTION.md` — checklist d'execution standard
- `bundles/claude-artifacts/prompts/` — prompts specialises par type de GO
- `bundles/claude-artifacts/bundle_meta/manifest.json` — metadata structuree du pack
