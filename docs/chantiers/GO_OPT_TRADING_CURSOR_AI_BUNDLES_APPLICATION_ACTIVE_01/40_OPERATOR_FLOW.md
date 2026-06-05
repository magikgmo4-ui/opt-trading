---
doc_id: GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01_40_OPERATOR_FLOW
doc_type: chantier/operator_flow
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/OPERATOR_FLOW.md
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
---

# 40_OPERATOR_FLOW — Flux operateur Bundles cursor-ai

Le flux complet est defini dans `bundles/OPERATOR_FLOW.md`.

## Resume du flux

1. **Identifier source** — matiere a packager
2. **Classifier bundle** — type de bundle (reprise, operator pack, handoff, prompt, merge, closeout)
3. **Extraire contenu stable** — templates, regles, procedures (pas d'instances avec donnees reelles)
4. **Creer pack / docs** — `bundles/<name>/` ou `docs/chantiers/<GO_ID>/`
5. **Verifier no-runtime / no-secret** — checklist pre-commit
6. **Commit doc-only** — `git add`, `git commit`
7. **PR / merge** — `gh pr create`, `gh pr merge`
8. **Reprise** — sync local, mettre a jour la fiche de reprise

## Lien avec Claude artifacts

Le pack `bundles/claude-artifacts/` fournit les templates de prompts pour chaque etape :
- Template 1 (reprise) → Etape 1
- Template 4 (safety check) → Etape 5
- Template 3 (merge) → Etape 7
- Template 5 (handoff) → Etape 8

## Exemple : creer un nouveau bundle

```bash
# 1. Identifier source : docs existants, prompts, regles
# 2. Classifier : operator pack
# 3. Extraire : templates, pas d'instances

# 4. Creer pack
mkdir bundles/mon-pack
# Creer README.md, PROMPT_TEMPLATES.md, etc.

# 5. Verifier
git diff --cached --name-only | grep -vE "^(docs/|bundles/)"

# 6. Commit
git add bundles/mon-pack/
git commit -m "docs: add mon-pack bundle"

# 7. PR
gh pr create --title "docs: add mon-pack" --body "..." --base sot/mainline --head go/MON_GO
gh pr merge <NUM> --merge --delete-branch

# 8. Reprise
git fetch origin --prune && git checkout sot/mainline && git pull --rebase origin sot/mainline
```

## RISKS

- À qualifier.
