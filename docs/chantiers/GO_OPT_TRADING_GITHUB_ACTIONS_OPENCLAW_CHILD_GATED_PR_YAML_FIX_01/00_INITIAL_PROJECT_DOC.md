---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_YAML_FIX_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: github_actions
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_YAML_FIX_01
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
status: open
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_GITHUB_ACTIONS_OPENCLAW
MASTER_PROJECT_PLAN_ID: MPP_GITHUB_ACTIONS_OPENCLAW
PARENT_GO_ID: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
1_MASTER_TARGET: github_actions_openclaw
NEXT_GO: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_TEST_01
topic_keys:
  - opt-trading
  - github_actions
  - gated_pr
  - yaml_parsing
  - colon_fix
links:
  - .github/workflows/gated-pr.yml
---

# GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_YAML_FIX_01

## Objet

Corriger le parsing YAML de `.github/workflows/gated-pr.yml` en remplaçant la `run` inline problématique par un bloc YAML valide (`|`).

## État établi

- `GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_02` merged
- `workflow_dispatch` fonctionne — plus de HTTP 422
- Root cause identifiée : le `:` dans `PASS:` sur une ligne `run` inline est interprété comme un mapping YAML
- La ligne actuelle est : `run: 'echo "PASS: gated PR scope checks completed."'` — syntaxe correcte mais fragile

## Correctif

Remplacer la `run` inline par un bloc littéral YAML :

```yaml
# AVANT
run: 'echo "PASS: gated PR scope checks completed."'

# APRÈS
run: |
  echo "PASS: gated PR scope checks completed."
```

Le bloc `|` (literal block scalar) est le standard idiomatique YAML pour les commandes shell multilignes. GitHub Actions le recommande.

## FILE_SCOPE

Seuls les chemins listés dans `FILE_SCOPE.txt` sont modifiés.

## Validation locale

- `git status --short --branch` avant modification
- `git diff --check` — pas d'espaces parasites
- `git diff --name-only` — scope uniquement :
  - `.github/workflows/gated-pr.yml`
  - `docs/chantiers/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_YAML_FIX_01/**`
  - `docs/index/inbox/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_YAML_FIX_01.md`
- `grep "PASS:"` ne doit plus contenir la ligne `run: 'echo "PASS:...'`
- `python3 -c "import yaml; yaml.safe_load(...)"` — PASS

## 12_INVARIANTS

- Ne pas toucher admin-trading
- Ne pas installer de self-hosted runner
- Ne pas ajouter d'auto-merge
- Ne pas réintroduire `merge_group`
- Ne pas modifier les registres GitHub Actions sauf nécessité prouvée
- Ne pas modifier les index globaux sauf changement global prouvé
- Ne pas mélanger les fichiers DeskPro / Google Sheets / Data Center
- Pas de reset --hard
- Push forcé seulement avec --force-with-lease si nécessaire
- `sot/mainline` reste remote canonique

## NEXT_GO

`GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_TEST_01`
(seulement après PASS de la présente GO)

## NEXT_GO ensuite

`GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01`
