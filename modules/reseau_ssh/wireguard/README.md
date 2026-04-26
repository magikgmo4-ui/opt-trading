# reseau_ssh wireguard — payload interne WireGuard + firewall

## Family status (reseau_ssh*)
- Canonical top-level module: `reseau_ssh`
- Internal payload location: `modules/reseau_ssh/wireguard`
- Former prerequisite capabilities are now internalized under `modules/reseau_ssh/baseline`
- Archived legacy step1: `_archive/legacy_modules/reseau_ssh_step1`
- Reference decision: `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`

Prerequisite note: the WireGuard workflow assumes the baseline SSH/hosts layer is already in place through `cmd-reseau_ssh baseline-*` or equivalent.

## Role
This directory is not a published module surface.

It is an internal payload used by the canonical facade:
- published logic: `modules/reseau_ssh/scripts/*`
- internal data/docs/templates: `modules/reseau_ssh/wireguard/*`

## Goal
- Add a **management WireGuard network** between:
  - admin-trading (hub) → db-layer, student, (optional) cursor-ai
- Optionally tighten firewall rules safely (UFW on Linux; Windows firewall handled by WireGuard/OpenSSH already).

We keep it safe:
- **No LAN routing** by default (AllowedIPs = 10.66.66.0/24 only).
- Every command has a dry-run.
- Backups are created before writing configs.

## Quick start (Linux)
From the repo root or via installed aliases:
```bash
cmd-reseau_ssh wireguard-sanity
cmd-reseau_ssh wg-install
cmd-reseau_ssh wg-genkeys
cmd-reseau_ssh wg-render
cmd-reseau_ssh wg-apply
cmd-reseau_ssh wg-up
cmd-reseau_ssh wg-status
```

### Key exchange flow (recommended)
1) On each Linux client:
```bash
cmd-reseau_ssh wg-genkeys
cmd-reseau_ssh wg-showpub
```
Copy the `PUBLIC KEY:` lines to admin-trading.

2) On admin-trading:
- Put peer public keys into:
`/opt/trading/data/reseau_ssh/wireguard/peers/<hostname>.pub`
Then:
```bash
cmd-reseau_ssh wg-render
cmd-reseau_ssh wg-apply
cmd-reseau_ssh wg-up
cmd-reseau_ssh wg-status
```

3) On clients:
- Put hub public key into:
`/opt/trading/data/reseau_ssh/wireguard/hub/admin-trading.pub`
Then:
```bash
cmd-reseau_ssh wg-render
cmd-reseau_ssh wg-apply
cmd-reseau_ssh wg-up
cmd-reseau_ssh wg-status
```

## Windows (cursor-ai)
See `windows/README_WINDOWS_WIREGUARD.md`.
We generate a ready-to-import config:
```bash
cmd-reseau_ssh wg-render-windows
```

## Firewall (optional, safe)
We DO NOT auto-enable "deny incoming" unless you run:
```bash
cmd-reseau_ssh fw-apply
```
First:
```bash
cmd-reseau_ssh fw-dry-run
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
cmd-reseau_ssh wg-down
sudo rm -f /etc/wireguard/wg-mgmt.conf   # optional
```

## Target
1 module canonique par famille.
