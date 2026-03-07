# Git Ops - Quick Reference

| Action | Machine | Commande |
|---|---|---|
| **Status Windows** | Windows (PowerShell) | `.\scripts\git_ops\git_commit_push_windows.ps1 -ShowStatusOnly` |
| **Commit & Push** | Windows (PowerShell) | `.\scripts\git_ops\git_commit_push_windows.ps1 -Paths "file1,file2" -CommitMessage "msg"` |
| **Pull Update** | Linux (Bash) | `bash scripts/git_ops/git_pull_update_linux.sh` |
| **Pull with Restore** | Linux (Bash) | `bash scripts/git_ops/git_pull_update_linux.sh --paths <file1> <file2>` |
| **Menu Sync** | Linux (Bash) | `bash scripts/git_ops/git_sync_menu.sh` |
| **Sanity Check** | Linux (Bash) | `bash scripts/git_ops/git_sync_sanity_check.sh` |
| **Status Short** | Linux (Bash) | `git status --short` |
| **Last Commit** | Linux (Bash) | `git log -1 --oneline` |

---
**Rappel** :
- `--paths` restaure (écrase) les modifications locales avant le pull.
- Utilisez `--ff-only` pour éviter les merges accidentels.
