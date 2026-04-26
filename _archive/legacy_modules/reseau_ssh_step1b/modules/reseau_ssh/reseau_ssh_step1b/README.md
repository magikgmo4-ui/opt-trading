# reseau_ssh — Step 1b (Apply: hosts + ssh config + key tests)

## Family status (reseau_ssh*)
- Not the canonical surface anymore (active continuity moved to top-level `reseau_ssh`)
- No longer used by the canonical `baseline-*` commands
- Legacy / doc pre-step: `_archive/legacy_modules/reseau_ssh_step1`
- Reference decision: `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`

## Current classification
- `archive_backup`
- not a valid final survivor
- archived repo-side after final audit of non-published helpers
- machine-side copies may still remain until dedicated cleanup

Linux:
- Safely installs/updates:
  - /etc/hosts (adds a managed block)
  - ~/.ssh/config (canonical aliases)
- Optional: enforce hostname
- Sanity checks + best-effort connectivity tests

Windows (cursor-ai / Dell):
- Updates hosts file
- Writes C:\Users\ghost\.ssh\config
- Optional:
  - Enable OpenSSH Server + firewall rule TCP/22
  - Pull a keys bundle from admin-trading to populate authorized_keys

Recommended order:
1) admin-trading: apply_linux --apply
2) student: apply_linux --apply
3) db-layer: apply_linux --apply
4) cursor-ai: apply_cursor_ai.ps1 (PowerShell admin)

## Target
1 module canonique par famille.
