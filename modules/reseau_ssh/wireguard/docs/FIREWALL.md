# Firewall plan (Linux / UFW)

We keep it conservative.

## Hub (admin-trading)
- allow OpenSSH (tcp/22) from LAN + WG net
- allow WireGuard UDP/51820 from LAN
- optionally restrict other ports later

## Client (db-layer, student)
- allow OpenSSH (tcp/22) from LAN + WG net
- allow outbound UDP/51820 to hub (usually already allowed)
- if you set default deny incoming, keep OpenSSH allowed
