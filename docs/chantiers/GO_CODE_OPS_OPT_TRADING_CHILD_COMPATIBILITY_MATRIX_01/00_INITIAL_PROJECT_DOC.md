---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: matrix_v1_complete
topic_keys:
  - opt-trading
  - code_ops
  - compatibility
  - debian
  - windows
  - wsl
  - tmux
  - github_actions
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/40_COMPATIBILITY_MATRIX.md
  - docs/registry/CODE_REGISTRY.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01/10_COMPATIBILITY_MATRIX.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01/20_COMPAT_FINDINGS.md
---

# GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Renseigner la matrice de compatibilité pour les surfaces clés du registre,
avant tout batch de refactor.

## 6_FINAL_TARGET

Matrice renseignée (v1). Surfaces à risque identifiées. Contraintes documentées
pour chaque batch de refactor futur.

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| Audit effectué le | 2026-05-28 |
| Méthode | git grep + lecture code + inspection workflows |
| Mutation code | aucune |
| Surfaces auditées | Debian/Bash, Windows/WSL, tmux, GHA, JSON, UTF-8 |

## Résultats clés

| Surface | Verdict global |
|---|---|
| Debian / Bash | PASS — 771/773 scripts `env bash`, 2 à corriger |
| Windows natif | PASS_WITH_LIMITS — Python portable ; Bash → WSL/Git Bash requis |
| WSL | PASS — fonctionne, tmux dispo |
| tmux | PASS — Debian/WSL ; N/A Windows natif |
| GitHub Actions | PASS — ubuntu-latest only ; pas de CI Windows/macOS |
| JSON outputs | PASS_WITH_LIMITS — `ensure_ascii=False` absent des modules HIGH |
| UTF-8 | PASS — Python 3 natif UTF-8 |
| Path handling | PASS — 329 fichiers pathlib/os.path.join |

## 11_KEY_DECISIONS

| Sujet | Décision |
|---|---|
| 2 scripts `#!/bin/bash` | REWORK dans batch dédié |
| ensure_ascii HIGH modules | PASS_WITH_LIMITS — trading data ASCII, risque faible |
| CI Windows/macOS | N/A — pas de besoin prouvé |
| tmux Windows | N/A — usage Linux/WSL uniquement |

## 15_REMAINING_GAP

- 2 scripts `#!/bin/bash` à migrer vers `#!/usr/bin/env bash`
- `ensure_ascii=False` non systématique dans modules HIGH — acceptable mais à noter

## 16_TODO

1. corriger les 2 shebangs dans un batch dédié (faible risque) ;
2. documenter la contrainte ensure_ascii dans les runbooks refactor ;
3. ouvrir `GO_CODE_OPS_OPT_TRADING_CHILD_SAFE_REFACTOR_BATCH_01`.

## 17_RESUME_POINT

```text
Matrice v1 complète. Aucun code modifié.
NEXT_GO = GO_CODE_OPS_OPT_TRADING_CHILD_SAFE_REFACTOR_BATCH_01
ou corriger les 2 shebangs en lot mineur.
```
