---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01_DELETION_PROOF
doc_type: deletion_proof
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01
updated_at: 2026-05-28
---

# 10_DELETION_PROOF

## Preuves d'obsolescence (confirmées)

| Vérification | Commande | Résultat |
|---|---|---|
| 0 consommateur externe | `git grep "apply_desk_pro" -- "*.py" "*.sh"` hors scripts | 0 résultat |
| routes.py déjà patché | `grep -n "toolbox" modules/desk_pro/api/routes.py` | PRÉSENT lignes 299, 300, 304, 313, 321, 322, 353, 354 |
| Commits d'application | `git log --oneline --all -- scripts/apply_desk_pro_*.sh` | `4e01dc4a`, `3ef76eb3` |

## Scripts supprimés (git rm)

```
scripts/apply_desk_pro_toolbox_patch.sh      (58 lignes)
scripts/apply_desk_pro_ui_inject_patch.sh    (74 lignes)
scripts/apply_desk_pro_ui_plus_patch.sh      (64 lignes)
scripts/apply_desk_pro_ui_toolbox_fix.sh     (63 lignes)
scripts/apply_desk_pro_ui_toolbox_fix_v2.sh  (71 lignes)
scripts/apply_desk_pro_ui_toolbox_fix_v3.sh  (71 lignes)
scripts/apply_desk_pro_ui_toolbox_fix_v4.sh  (71 lignes)
scripts/apply_desk_pro_ui_toolbox_final.sh   (71 lignes)
```

**Total supprimé : 8 fichiers, ~543 lignes.**

## Rollback

```bash
git revert <merge_commit_de_cette_PR>
```

Les scripts seront restaurés. Inutiles après revert car `routes.py:299-354` reste intact.
