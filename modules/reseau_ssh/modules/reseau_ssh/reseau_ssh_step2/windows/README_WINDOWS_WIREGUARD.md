# Windows WireGuard (cursor-ai)

## Prereqs
- Install "WireGuard for Windows" (official).
- OpenSSH Server already installed/enabled (you did this in Step 1b).

## How to import config
1) On a Linux machine with the module, generate the Windows config:
   ```bash
   ./scripts/reseau_ssh_cmd.sh wg-render-windows
   ```
   Output:
   - `/opt/trading/data/reseau_ssh/wireguard/windows/cursor-ai_wg-mgmt.conf`

2) Copy that file to Windows (cursor-ai), then:
   - Open WireGuard app → "Import tunnel(s) from file" → choose `cursor-ai_wg-mgmt.conf`.
   - Activate tunnel.

## Notes
- If your Windows account is in the local Administrators group, OpenSSH may use:
  `C:\ProgramData\ssh\administrators_authorized_keys`
  (we already handled this in Step 1b).
