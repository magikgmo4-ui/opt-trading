# Run as Administrator
$lan = "192.168.16.0/24"

# SSH inbound from LAN (if you run OpenSSH server on Windows)
New-NetFirewallRule -DisplayName "reseau_ssh SSH 22 TCP In (LAN)" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 22 -RemoteAddress $lan -Profile Any -ErrorAction SilentlyContinue | Out-Null

# WireGuard inbound from LAN
New-NetFirewallRule -DisplayName "reseau_ssh WireGuard 51820 UDP In (LAN)" -Direction Inbound -Action Allow -Protocol UDP -LocalPort 51820 -RemoteAddress $lan -Profile Any -ErrorAction SilentlyContinue | Out-Null

Write-Host "OK: firewall rules applied (LAN=$lan)"
