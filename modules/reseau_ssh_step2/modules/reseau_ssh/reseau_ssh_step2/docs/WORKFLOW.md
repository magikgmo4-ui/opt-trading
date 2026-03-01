# WORKFLOW (Step 2)

## Gate A — WireGuard only
1) Install wireguard (`wg-install`)
2) Generate keys (`wg-genkeys`) on each host
3) Exchange public keys (copy/paste or scp)
4) Render configs (`wg-render`)
5) Apply + start (`wg-apply`, `wg-up`)
6) Sanity checks (`sanity`, `wg-status`)

## Gate B — Optional firewall tighten
1) Dry-run firewall plan (`fw-dry-run`)
2) Apply firewall (`fw-apply`)
3) Re-test SSH on LAN and WG

## Safety
Keep an open session to undo:
- `./scripts/reseau_ssh_cmd.sh wg-down`
- `sudo ufw disable`
