---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_02_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: github_actions
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_02
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
  - removal
links:
  - .github/workflows/gated-pr.yml
---

# GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_02

## Objet

Stabiliser `gated-pr.yml` en supprimant temporairement `merge_group` afin de valider d'abord :
1. `workflow_dispatch` manuel
2. `pull_request` checks
3. reporting correct des jobs `gate/*`

## État établi (pré-merge)

- master plan github_actions_openclaw merged
- registry GitHub Actions merged
- registry validation merged
- bridge OpenClaw ↔ GitHub Actions merged
- dry-run OpenClaw positif PASS merged
- gated-pr.yml + FILE_SCOPE + no-overlap merged
- root transport cleanup merged
- GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_FIX_01 merged
- gated-pr.yml existe et est actif dans GitHub Actions
- mais les runs gated-pr échouent toujours en 0s avec :
  "This run likely failed because of a workflow file issue"
- `gh workflow run gated-pr.yml` retourne encore :
  HTTP 422: Workflow does not have 'workflow_dispatch' trigger
- le fichier contient pourtant `workflow_dispatch`
- donc le parsing global du workflow est encore invalide

## Hypothèse principale

Le bloc `merge_group` reste incompatible ou mal parsé :
```yaml
merge_group:
  types:
    - checks_requested
  branches:
    - sot/mainline
```

## Correctif

1. Retirer complètement le bloc `merge_group` de `.github/workflows/gated-pr.yml`
2. Conserver `pull_request` vers `sot/mainline`
3. Conserver `workflow_dispatch` explicite avec input `reason`
4. Conserver les jobs :
   - `gate/preflight`
   - `gate/file-scope`
   - `gate/no-lock-overlap`
   - `gate/tests`

## Bloc `on` final attendu

```yaml
on:
  pull_request:
    branches:
      - sot/mainline
    types:
      - opened
      - synchronize
      - reopened
      - ready_for_review
  workflow_dispatch:
    inputs:
      reason:
        description: Manual gated-pr activation test
        required: false
        default: manual
```

## FILE_SCOPE

Seuls les chemins listés dans `FILE_SCOPE.txt` sont modifiés.

## 6_FINAL_TARGET

- `merge_group` supprimé
- `pull_request` vers `sot/mainline` conservé
- `workflow_dispatch` avec input `reason` explicite conservé
- Tous les jobs `gate/*` conservés
- PR vers `sot/mainline`

## Validation locale

- `git diff --check`
- `gh workflow view gated-pr.yml --yaml` (doit afficher `workflow_dispatch` explicite, pas de `merge_group`)
- Vérifier que le YAML ne contient plus `merge_group`
- Vérifier que `workflow_dispatch` est toujours présent avec input `reason`
- Ouvrir PR vers `sot/mainline`

## Validation attendue après merge

```bash
gh workflow run gated-pr.yml --ref sot/mainline -f reason=manual
gh run list --workflow gated-pr.yml --limit 5
```

Ouvrir une micro-PR de test si `workflow_dispatch` fonctionne.
`gh pr checks --watch` doit afficher les checks `gate/*` sur la micro-PR.

## 12_INVARIANTS

- Ne pas toucher admin-trading
- Ne pas installer de self-hosted runner
- Ne pas ajouter d'auto-merge
- Ne pas modifier les registres GitHub Actions sauf nécessité prouvée
- Ne pas modifier les index globaux sauf changement global prouvé
- Pas de reset --hard
- push forcé seulement avec --force-with-lease si nécessaire
- sot/mainline reste remote canonique
- Ne pas réintroduire `merge_group` dans ce GO

## NEXT_GO

`GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01`
(seulement après PASS de la présente GO)

## NEXT_GO optionnel (plus tard)

`GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_MERGE_GROUP_REINTRODUCTION_01`
