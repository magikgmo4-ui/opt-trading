---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_PARENT_CLOSE_GATE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_PARENT_CLOSE_GATE_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: closed
lifecycle_stage: done
topic_keys:
  - opt-trading
  - code_ops
  - close_gate
  - rebase
  - parent_closeout
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_PARENT_CLOSE_GATE_01/10_PARENT_CLOSE_GATE.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_PARENT_CLOSE_GATE_01/20_BRANCH_REBASE_OR_SYNC_REPORT.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_PARENT_CLOSE_GATE_01/30_VALIDATION_REPORT.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/90_PARENT_CLOSEOUT.md
---

# GO_CODE_OPS_OPT_TRADING_CHILD_PARENT_CLOSE_GATE_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Fermer proprement le parent `GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01` :
1. Produire le close-gate formel (10_PARENT_CLOSE_GATE.md)
2. Réaligner la branche sur `sot/mainline` (rebase)
3. Valider l'état final (30_VALIDATION_REPORT.md)
4. Émettre le closeout parent (90_PARENT_CLOSEOUT.md)

## 6_FINAL_TARGET

Branche réalignée, parent fermé, PR-ready.

## 3_CONTRAINTES

- Ne pas ouvrir de nouveau refactor fonctionnel
- Ne pas supprimer les .bak (sudo hors portée)
- CLEANUP_BAK_01 documenté comme remaining gap hors automatisation
- Réaligner via `git rebase origin/sot/mainline` (pas merge)
- `git push --force-with-lease` après rebase propre
