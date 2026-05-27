---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: github_actions
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_01
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
NEXT_GO: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01
topic_keys:
  - opt-trading
  - github_actions
  - openclaw
  - gated_pr
  - workflow_dispatch
  - merge_group
links:
  - .github/workflows/gated-pr.yml
---

# GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_01

## Objet

Corriger l'activation/parsing GitHub Actions de `.github/workflows/gated-pr.yml`.

Le workflow existe et est actif dans GitHub Actions, mais les runs échouent en 0s
avec "workflow file issue". `gh workflow run gated-pr.yml` retourne :
```
HTTP 422: Workflow does not have 'workflow_dispatch' trigger
```

## État établi (pré-merge)

- master plan github_actions_openclaw merged
- registry GitHub Actions merged
- registry validation merged
- bridge OpenClaw ↔ GitHub Actions merged
- dry-run OpenClaw positif PASS merged
- gated-pr.yml + FILE_SCOPE + no-overlap merged
- root transport cleanup merged
- gated-pr.yml existe et est active dans GitHub Actions
- mais les runs échouent en 0s avec "workflow file issue"
- `gh workflow run gated-pr.yml` retourne HTTP 422

## Hypothèse principale

Le bloc `merge_group` actuel est invalide ou mal reconnu :
```yaml
merge_group:
  branches:
    - sot/mainline
```

## Correctif

1. Remplacer `merge_group` par une syntaxe valide avec `types: [checks_requested]`
2. Rendre `workflow_dispatch` explicite avec un input `reason`
3. Conserver les jobs existants : `gate/preflight`, `gate/file-scope`, `gate/no-lock-overlap`, `gate/tests`

## FILE_SCOPE

Seuls les chemins listés dans `FILE_SCOPE.txt` sont modifiés.

## 6_FINAL_TARGET

- `merge_group` avec `types: [checks_requested]` valide
- `workflow_dispatch` avec input `reason` explicite
- Tous les jobs `gate/*` conservés
- PR vers `sot/mainline`

## Validation locale

- `git diff --check`
- `gh workflow view gated-pr.yml --yaml` (doit afficher `workflow_dispatch` explicite)
- Ouvrir PR vers `sot/mainline`

## Validation attendue après merge

```bash
gh workflow run gated-pr.yml --ref sot/mainline -f reason=manual
gh run list --workflow gated-pr.yml --limit 5
```

`gh pr checks --watch` doit afficher les checks `gate/*`.

## 12_INVARIANTS

- Ne pas toucher admin-trading
- Ne pas installer de self-hosted runner
- Ne pas ajouter d'auto-merge
- Ne pas modifier les registres GitHub Actions sauf nécessité prouvée
- Ne pas modifier les index globaux sauf changement global prouvé
- Pas de reset --hard
- push forcé seulement avec --force-with-lease si nécessaire
- sot/mainline reste remote canonique

## NEXT_GO

`GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01`
(seulement après PASS de la présente GO)
