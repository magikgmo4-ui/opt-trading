---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: automation_ops
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01
parent_go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: open
lifecycle_stage: in_progress
topic_keys:
  - legacy_scripts
  - desk_pro
  - cleanup
  - automation_ops
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
base_branch: sot/mainline
working_branch: go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01
links:
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01/10_DELETION_PROOF.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01/20_ACCEPTANCE_REPORT.md
---

# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01 — INITIAL_PROJECT_DOC

## 1_OBJECTIF

Supprimer les 8 scripts `apply_desk_pro_*.sh` (B06 du JOBS_DEDUP_AUDIT_01).  
Preuve établie : `modules/desk_pro/api/routes.py:299-354` contient déjà le résultat.

## 2_PREUVE_D_OBSOLESCENCE

| Critère | Résultat |
|---|---|
| `git grep "apply_desk_pro" -- "*.py" "*.sh"` hors scripts eux-mêmes | 0 résultat |
| `grep "toolbox" modules/desk_pro/api/routes.py` | PRÉSENT lignes 299-354 |
| Commits d'application | `4e01dc4a`, `3ef76eb3` |

## 3_SCRIPTS_A_SUPPRIMER

```
scripts/apply_desk_pro_toolbox_patch.sh
scripts/apply_desk_pro_ui_inject_patch.sh
scripts/apply_desk_pro_ui_plus_patch.sh
scripts/apply_desk_pro_ui_toolbox_fix.sh
scripts/apply_desk_pro_ui_toolbox_fix_v2.sh
scripts/apply_desk_pro_ui_toolbox_fix_v3.sh
scripts/apply_desk_pro_ui_toolbox_fix_v4.sh
scripts/apply_desk_pro_ui_toolbox_final.sh
```

## 4_ROLLBACK

`git revert <merge_commit>` — restaure les 8 scripts.  
Inutiles après revert car routes.py reste patché.

## 5_SUCCESS_CRITERIA

```text
PASS_CLEANUP_LEGACY_SCRIPTS_01
→ 8 scripts supprimés (git rm)
→ 0 consommateur cassé
→ JOBS_REGISTRY Section 6 mise à jour (deprecated → deleted)
NEXT_GO = parent closeout ou ADD_TEST batch
```
