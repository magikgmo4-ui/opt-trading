---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_40_USAGE_WORKFLOW
doc_type: chantier/usage_workflow
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
  - bundles/claude-artifacts/REPRISE_TEMPLATE.md
  - bundles/claude-artifacts/CHECKLIST_EXECUTION.md
  - bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md
---

# 40_USAGE_WORKFLOW

## Ordre de lecture recommande

1. `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
2. `10_SOURCE_STATE.md`
3. `20_OPERATOR_PACK_SPEC.md`
4. `bundles/claude-artifacts/README.md`
5. `bundles/claude-artifacts/PROMPT_TEMPLATES.md`
6. `bundles/claude-artifacts/REPRISE_TEMPLATE.md`
7. `bundles/claude-artifacts/NO_COMMIT_RULES.md`
8. `bundles/claude-artifacts/CHECKLIST_EXECUTION.md`

## Workflow operateur

### 1. Sync Git

```bash
git fetch --all --prune
git status --short --branch
git switch sot/mainline
git pull --rebase origin sot/mainline
git switch go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
```

### 2. Valider le routage machine

- Confirmer que la demande reste dans `cursor-ai`.
- Refuser tout passage implicite vers `admin-trading`.
- Garder TradingView MCP ferme et `DOC_OPS BLOCKED` intact.

### 3. Produire ou reprendre un GO doc-only

- Utiliser `PROMPT_TEMPLATES.md` template 1 pour la reprise.
- Utiliser `REPRISE_TEMPLATE.md` pour la fiche de reprise.
- Documenter uniquement dans `docs/` et `bundles/`.

### 4. Verifier les limites avant review

- Utiliser `PROMPT_TEMPLATES.md` template 4 pour le no-runtime check.
- Executer `CHECKLIST_EXECUTION.md`.
- Verifier aussi `bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md`.

### 5. Review, PR et handoff

- Utiliser `PROMPT_TEMPLATES.md` template 2 avant merge.
- Utiliser `PROMPT_TEMPLATES.md` template 3 pour le merge doc-only.
- Utiliser `PROMPT_TEMPLATES.md` template 5 pour le handoff IDE.

## Bornes d'escalade

- Si la demande exige `admin-trading`, arreter et demander une ouverture explicite.
- Si la demande touche runtime, `systemd`, webhook, risk engine ou payload live, sortir du perimetre de ce pack.
- Si un doute apparait sur une branche historique ou Git audit, rester en lecture seule et renvoyer vers les references.
