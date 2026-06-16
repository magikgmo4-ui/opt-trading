---
doc_id: OPT_TRADING_MATRICE_DOC_OPS_CHILD_ALWAYS_ON_GATES_01_INITIAL
doc_type: chantier_initial_project_doc
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MATRICE_DOC_OPS_CHILD_ALWAYS_ON_GATES_01
status: initial
lifecycle_stage: ouverture
topic_keys:
  - opt-trading
  - governance
  - matrice_doc_ops
  - always_on_gates
  - child
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-06-16
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md
---

# GO_OPT_TRADING_MATRICE_DOC_OPS_CHILD_ALWAYS_ON_GATES_01

## 1_MASTER_TARGET

matrice_doc_ops_governance

## 3_INITIAL_NEED

Rendre la matrice applicable en tout temps — PR, IDE, SSH machine, fix simple, patch, runtime, closeout.

PR #1194 a prouvé le gap : le gate détecte l'écart mais le merge a été possible sans blocage.

## 4_MASTER_PROJECT_PLAN

1. Gouvernance : ajouter section "Application permanente" dans la matrice maître
2. Session gate : ajouter section "Gate permanent avant PR" dans SESSION_DOCUMENTATION_GATE.md
3. Chantier : créer 00_INITIAL_PROJECT_DOC.md, FILE_SCOPE.txt, 90_CLOSEOUT.md
4. Index inbox : créer entrée courte docs/index/inbox/<GO_ID>.md
5. GitHub gates : activer required checks dans GitHub Ruleset (post-merge)

## 6_FINAL_TARGET

Always-on gates appliqués à toute modification durable du repo.

## 12_INVARIANTS

- PR mergée ≠ chantier fermé
- Aucun bypass autorisé
- Pas de seconde matrice créée
- Parent GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 non fermé

## 17_RESUME_POINT

Après merge de ce GO, activer les required checks côté GitHub Ruleset :

- gate/preflight
- gate/file-scope
- gate/no-lock-overlap
- gate/tests

(Pas réalisable dans ce GO — action GitHub UI/API hors repo.)
