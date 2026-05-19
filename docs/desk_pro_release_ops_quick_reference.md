# Desk Pro - Release Ops Quick Reference

Référence procédurale complète : `docs/desk_pro_release_ops_runbook.md`

| Action | Machine | Commande |
|---|---|---|
| **Freeze Tag** | Windows (PowerShell) | `.\scripts\release_ops\desk_pro_freeze_tag.ps1 -TagName v1.2.0 -TagMessage "Final Ops Pack"` |
| **Verify Tag** | Linux (Bash) | `bash scripts/release_ops/desk_pro_verify_tag_linux.sh v1.2.0` |
| **Menu Release** | Linux (Bash) | `bash scripts/release_ops/desk_pro_release_menu.sh` |
| **Sanity Check** | Linux (Bash) | `bash scripts/release_ops/desk_pro_release_sanity_check.sh` |
| **Show Tags** | Linux (Bash) | `git tag -n1 --sort=-v:refname | head -n 5` |
| **Show HEAD** | Linux (Bash) | `git show --no-patch --format="%h %cd %s"` |

Notes :
- Utiliser ce document comme aide-mémoire compacte, pas comme procédure complète.
- Le workflow détaillé, les cas d'erreur, et le scope de validation par machine vivent dans le runbook.
- La validation runtime finale `scripts/admin_trading/desk_pro_cmd.sh status` / `cmd-desk_pro_runner status` ne concerne que `admin-trading`.
