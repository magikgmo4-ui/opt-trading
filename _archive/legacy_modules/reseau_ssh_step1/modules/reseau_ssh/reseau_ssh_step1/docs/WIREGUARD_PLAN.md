## WireGuard plan (Step 2)

Target:
- Admin-trading runs WireGuard server
- All machines connect as peers

Proposed VPN subnet:
- 10.8.0.0/24

Peer IPs:
- admin-trading: 10.8.0.1
- student:      10.8.0.2
- msi:          10.8.0.3
- win:          10.8.0.4

Firewall principles:
- Allow UDP/51820 on server (LAN + optional WAN)
- Restrict SSH to LAN + VPN ranges
- Keep services (Desk/Perf) bound to LAN or VPN, not public
