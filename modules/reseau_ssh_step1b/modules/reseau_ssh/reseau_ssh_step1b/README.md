# reseau_ssh — Step 1b (Apply: hosts + ssh config + key tests)

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
