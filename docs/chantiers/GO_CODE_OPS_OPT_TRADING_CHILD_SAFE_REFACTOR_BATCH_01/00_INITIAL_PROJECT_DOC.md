---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_SAFE_REFACTOR_BATCH_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_SAFE_REFACTOR_BATCH_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: closed
lifecycle_stage: done
topic_keys:
  - opt-trading
  - code_ops
  - shebang
  - portability
  - github_actions
  - python_version
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01/10_COMPATIBILITY_MATRIX.md
  - docs/registry/CODE_REGISTRY.md
---

# GO_CODE_OPS_OPT_TRADING_CHILD_SAFE_REFACTOR_BATCH_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Appliquer les corrections mécaniques identifiées par la matrice de compatibilité :
- 2 shebangs `#!/bin/bash` → `#!/usr/bin/env bash` (REWORK section 3)
- 3 workflows GHA `python-version: "3.x"` → `"3.11"` (recommandation section 4)

Aucune mutation logique — changements purement portabilité/normalisation.

## 6_FINAL_TARGET

5 fichiers corrigés. Tests syntaxiques PASS. Contraintes matrice respectées.

## 3_SCOPE

| # | Fichier | Type | Avant | Après |
|---|---|---|---|---|
| R01 | `modules/desk_pro/desk_pro_dry_run.sh` | shebang | `#!/bin/bash` | `#!/usr/bin/env bash` |
| R02 | `scripts/ai/workers/run_task.sh` | shebang | `#!/bin/bash` | `#!/usr/bin/env bash` |
| R03 | `.github/workflows/openclaw-mcp-policy-static-validator.yml` | GHA | `"3.x"` | `"3.11"` |
| R04 | `.github/workflows/strict-workers-validate.yml` | GHA | `"3.x"` | `"3.11"` |
| R05 | `.github/workflows/gh-actions-registry-validation.yml` | GHA | `"3.x"` | `"3.11"` |

## 4_CONTRAINTES

- Ne pas toucher à la logique des scripts — shebang line 1 uniquement
- Ne pas modifier les workflows au-delà de `python-version`
- Préserver `\\latest.json` dans `fleet_orchestrator.py` (non concerné ici)
- Préserver tmux checks (non concernés ici)

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| Source des corrections | Matrice compat v1 (sections 3 et 4) |
| Risque | FAIBLE — aucune mutation logique |
| Rollback | `git revert <commit>` — changements atomiques |

## 11_KEY_DECISIONS

| Sujet | Décision |
|---|---|
| Scope batch | 5 fichiers, 2 types (shebang + GHA) |
| Test post-mutation | `bash -n` syntax check pour les scripts shell |
| Homogénéisation GHA | 3.x → 3.11 (version déjà utilisée par `openclaw-skill-policy-warning-only.yml`) |

## 15_REMAINING_GAP

Après ce batch :
- D06 .bak — toujours BLOCKED_PERMISSIONS (hors scope)
- Entrées BLOCKED registry à qualifier (hors scope)
- ADD_TEST batch A04/A05/A06 (hors scope)

## 16_TODO

1. Appliquer R01–R05
2. `bash -n` sur R01, R02
3. Commit + push
4. Fermer GO

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| R01 desk_pro_dry_run.sh | DONE — shebang corrigé, bash -n PASS |
| R02 run_task.sh | DONE — shebang corrigé, bash -n PASS |
| R03 openclaw-mcp-policy-static-validator.yml | DONE — 3.x → 3.11 |
| R04 strict-workers-validate.yml | DONE — 3.x → 3.11 |
| R05 gh-actions-registry-validation.yml | DONE — 3.x → 3.11 |
| Mutation logique | aucune |

## 17_RESUME_POINT

```text
DONE — 5/5 corrections appliquées et vérifiées.
GO fermé.
```
