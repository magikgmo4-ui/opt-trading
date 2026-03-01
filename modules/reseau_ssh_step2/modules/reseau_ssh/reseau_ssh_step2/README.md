# reseau_ssh — Step 2 (WireGuard VPN + Firewall plan)

## Goal
- Add a **management WireGuard network** between:
  - admin-trading (hub) → db-layer, student, (optional) cursor-ai
- Optionally tighten firewall rules safely (UFW on Linux; Windows firewall handled by WireGuard/OpenSSH already).

We keep it safe:
- **No LAN routing** by default (AllowedIPs = 10.66.66.0/24 only).
- Every command has a dry-run.
- Backups are created before writing configs.

## Quick start (Linux)
From the module dir:
```bash
./scripts/reseau_ssh_cmd.sh sanity
./scripts/reseau_ssh_cmd.sh wg-install   # installs wireguard packages if missing
./scripts/reseau_ssh_cmd.sh wg-genkeys   # generates local keys (private stays local)
./scripts/reseau_ssh_cmd.sh wg-render    # renders config from inventory + known peer pubs
./scripts/reseau_ssh_cmd.sh wg-apply     # writes /etc/wireguard/wg-mgmt.conf (backup first)
./scripts/reseau_ssh_cmd.sh wg-up        # start wg-mgmt
./scripts/reseau_ssh_cmd.sh wg-status
```

### Key exchange flow (recommended)
1) On each Linux client:
```bash
./scripts/reseau_ssh_cmd.sh wg-genkeys
./scripts/reseau_ssh_cmd.sh wg-showpub
```
Copy the `PUBLIC KEY:` lines to admin-trading.

2) On admin-trading:
- Put peer public keys into:
`/opt/trading/data/reseau_ssh/wireguard/peers/<hostname>.pub`
Then:
```bash
./scripts/reseau_ssh_cmd.sh wg-render
./scripts/reseau_ssh_cmd.sh wg-apply
./scripts/reseau_ssh_cmd.sh wg-up
./scripts/reseau_ssh_cmd.sh wg-status
```

3) On clients:
- Put hub public key into:
`/opt/trading/data/reseau_ssh/wireguard/hub/admin-trading.pub`
Then:
```bash
./scripts/reseau_ssh_cmd.sh wg-render
./scripts/reseau_ssh_cmd.sh wg-apply
./scripts/reseau_ssh_cmd.sh wg-up
./scripts/reseau_ssh_cmd.sh wg-status
```

## Windows (cursor-ai)
See `windows/README_WINDOWS_WIREGUARD.md`.
We generate a ready-to-import config:
```bash
./scripts/reseau_ssh_cmd.sh wg-render-windows
```

## Firewall (optional, safe)
We DO NOT auto-enable "deny incoming" unless you run:
```bash
./scripts/reseau_ssh_cmd.sh fw-apply
```
First:
```bash
./scripts/reseau_ssh_cmd.sh fw-dry-run
```

## Files written
- Linux: `/etc/wireguard/wg-mgmt.conf` (backup created)
- Linux: optional UFW rules if `fw-apply`
- Data dir:
  - `/opt/trading/data/reseau_ssh/wireguard/keys/`
  - `/opt/trading/data/reseau_ssh/wireguard/peers/`
  - `/opt/trading/data/reseau_ssh/wireguard/hub/`
  - `/opt/trading/data/reseau_ssh/wireguard/windows/`

## Rollback
```bash
./scripts/reseau_ssh_cmd.sh wg-down
sudo rm -f /etc/wireguard/wg-mgmt.conf   # optional
```
