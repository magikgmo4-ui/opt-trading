# Step 2 Plan (WireGuard + Firewall)

## Network
- LAN: 192.168.16.0/24
- WireGuard mgmt: 10.66.66.0/24
  - admin-trading: 10.66.66.1
  - db-layer:      10.66.66.2
  - student:       10.66.66.3
  - cursor-ai:     10.66.66.4 (optional)

## Design
Hub-and-spoke:
- admin-trading listens on UDP/51820 on LAN.
- Clients connect to 192.168.16.155:51820.

AllowedIPs:
- By default, only 10.66.66.0/24. (No LAN routing.)

## Firewall policy (Linux/UFW)
Minimum needed:
- allow TCP/22 from LAN + WG
- allow UDP/51820 from LAN (hub) or to hub (clients)
- allow established/related

We provide commands but keep it optional.
