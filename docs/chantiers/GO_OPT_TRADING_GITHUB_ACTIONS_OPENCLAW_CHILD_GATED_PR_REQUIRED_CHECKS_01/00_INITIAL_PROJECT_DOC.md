---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: github_actions
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01
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
NEXT_GO: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_OPERATIONAL_01
topic_keys:
  - opt-trading
  - github_actions
  - gated_pr
  - required_checks
  - branch_protection
links:
  - .github/workflows/gated-pr.yml
---

# GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01

## Objet

Documenter et préparer l'activation des required checks sur `sot/mainline` pour les 4 jobs `gate/*` du workflow `gated-pr.yml`.

## État établi

- `gated-pr.yml` merged et actif
- `workflow_dispatch` fonctionnel
- Micro-PR #788 a validé les 4 checks `gate/*` en PASS
  - `gate/preflight` ✅
  - `gate/file-scope` ✅
  - `gate/no-lock-overlap` ✅
  - `gate/tests` ✅

## Checks requis à documenter

| Check | Job dans gated-pr.yml | Description |
|---|---|---|
| `gate/preflight` | `gate-preflight` | Valide la cible PR et liste les fichiers modifiés |
| `gate/file-scope` | `gate-file-scope` | Vérifie qu'un seul GO est actif et que les fichiers sont dans son FILE_SCOPE |
| `gate/no-lock-overlap` | `gate-no-lock-overlap` | Vérifie qu'aucun autre GO ne revendique les mêmes fichiers |
| `gate/tests` | `gate-tests` | Diff hygiene + message de validation final |

## Livrables

1. `00_INITIAL_PROJECT_DOC.md` — ce fichier
2. `REQUIRED_CHECKS_POLICY.md` — politique des required checks
3. `GITHUB_UI_STEPS.md` — étapes pour l'activation manuelle via l'UI GitHub
4. `ROLLBACK_PLAN.md` — procédure de rollback
5. Inbox entry

## Contraintes

- Ne pas activer auto-merge
- Ne pas réintroduire `merge_group`
- Ne pas toucher admin-trading
- Ne pas modifier OpenClaw
- Ne pas modifier les index globaux sauf nécessité prouvée
- Ce GO est doc-only — la configuration GitHub UI est manuelle

## NEXT_GO

`GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_OPERATIONAL_01`
