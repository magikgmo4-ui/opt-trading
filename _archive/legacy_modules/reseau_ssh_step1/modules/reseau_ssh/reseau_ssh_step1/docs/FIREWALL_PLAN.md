## Firewall plan (Step 2)

Linux (UFW recommended):
- default deny incoming
- allow outgoing
- allow OpenSSH from LAN (192.168.16.0/24) and VPN (10.8.0.0/24)
- allow WireGuard UDP/51820 (server)

Windows:
- if using OpenSSH server: allow TCP/22 inbound from LAN/VPN
- optional: allow ShareX folder pull/push ports if needed

We will generate exact commands per host in Step 2.
