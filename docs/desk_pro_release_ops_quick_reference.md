# Desk Pro - Release Ops Quick Reference

| Action | Machine | Commande |
|---|---|---|
| **Freeze Tag** | Windows (PowerShell) | `.\scripts\release_ops\desk_pro_freeze_tag.ps1 -TagName v1.2.0 -TagMessage "Final Ops Pack"` |
| **Verify Tag** | Linux (Bash) | `bash scripts/release_ops/desk_pro_verify_tag_linux.sh v1.2.0` |
| **Menu Release** | Linux (Bash) | `bash scripts/release_ops/desk_pro_release_menu.sh` |
| **Sanity Check** | Linux (Bash) | `bash scripts/release_ops/desk_pro_release_sanity_check.sh` |
| **Show Tags** | Linux (Bash) | `git tag -n1 --sort=-v:refname | head -n 5` |
| **Show HEAD** | Linux (Bash) | `git show --no-patch --format="%h %cd %s"` |

---
**Workflow**
1. **Windows** : Commit propre -> `desk_pro_freeze_tag.ps1` -> Push.
2. **Linux** : `git fetch --tags` -> `desk_pro_verify_tag_linux.sh`.
