\
<#
reseau_ssh Step 1b — cursor-ai (Dell Windows)
Run in elevated PowerShell for hosts/OpenSSH parts.
#>

param(
  [string]$UserHome = $env:USERPROFILE,
  [switch]$EnableOpenSSHServer,
  [switch]$PullKeysBundle,
  [string]$AdminTradingHost = "admin-trading",
  [string]$KeysBundleRemotePath = "~/reseau_ssh_keys_bundle.pub"
)

$ErrorActionPreference = "Stop"

function OK($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function WARN($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function INFO($m){ Write-Host "[INFO] $m" }

$HostsPath = "$env:WINDIR\System32\drivers\etc\hosts"
$SshDir = Join-Path $UserHome ".ssh"
$SshConfig = Join-Path $SshDir "config"
$AuthorizedKeys = Join-Path $SshDir "authorized_keys"

$BlockBegin = "# === reseau_ssh BEGIN ==="
$BlockEnd   = "# === reseau_ssh END ==="
$BlockLines = @(
  $BlockBegin,
  "192.168.16.155  admin-trading",
  "192.168.16.179  db-layer",
  "192.168.16.103  student",
  "192.168.16.224  cursor-ai",
  $BlockEnd
)

$SshConfigContent = @"
# === reseau_ssh canonical config (Windows) ===
Host *
  ServerAliveInterval 30
  ServerAliveCountMax 3
  TCPKeepAlive yes
  IdentitiesOnly yes
  IdentityFile ~/.ssh/id_ed25519
  IdentityFile ~/.ssh/id_ed25519_fantome

Host admin-trading
  HostName 192.168.16.155
  User ghost
  Port 22

Host db-layer
  HostName 192.168.16.179
  User ghost
  Port 22

Host student
  HostName 192.168.16.103
  User student
  Port 22

Host cursor-ai
  HostName 192.168.16.224
  User ghost
  Port 22
"@

if (!(Test-Path $SshDir)) { New-Item -ItemType Directory -Path $SshDir | Out-Null; OK "Created $SshDir" }

$SshConfigContent | Set-Content -Encoding ascii $SshConfig
OK "Wrote $SshConfig"

try {
  $hostsText = Get-Content $HostsPath -Raw
  $pattern = [regex]::Escape($BlockBegin) + ".*?" + [regex]::Escape($BlockEnd)
  $hostsText2 = [regex]::Replace($hostsText, $pattern, "", "Singleline").TrimEnd()
  $hostsText2 = $hostsText2 + "`r`n`r`n" + ($BlockLines -join "`r`n") + "`r`n"
  Copy-Item $HostsPath "$HostsPath.bak.reseau_ssh.$(Get-Date -Format yyyyMMdd_HHmmss)" -Force
  $hostsText2 | Set-Content -Encoding ascii $HostsPath
  OK "Updated hosts file"
}
catch {
  WARN "Hosts update failed. Run as Administrator. $($_.Exception.Message)"
}

if ($EnableOpenSSHServer) {
  INFO "Enabling OpenSSH Server..."
  try { Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0 | Out-Null } catch { WARN "Capability add: $($_.Exception.Message)" }
  try {
    Start-Service sshd
    Set-Service -Name sshd -StartupType Automatic
    OK "sshd started + Automatic"
  } catch { WARN "sshd start failed: $($_.Exception.Message)" }

  try {
    if (-not (Get-NetFirewallRule -DisplayName "OpenSSH Server (sshd) reseau_ssh" -ErrorAction SilentlyContinue)) {
      New-NetFirewallRule -DisplayName "OpenSSH Server (sshd) reseau_ssh" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 22 -Profile Any | Out-Null
      OK "Firewall rule TCP/22 added"
    } else { OK "Firewall rule already exists" }
  } catch { WARN "Firewall step failed: $($_.Exception.Message)" }
}

if ($PullKeysBundle) {
  INFO "Pulling keys bundle from $AdminTradingHost:$KeysBundleRemotePath"
  $tmp = Join-Path $env:TEMP "reseau_ssh_keys_bundle.pub"
  try {
    scp "$AdminTradingHost`:$KeysBundleRemotePath" "$tmp" | Out-Null
    if (Test-Path $tmp) {
      Get-Content $tmp | Add-Content -Encoding ascii $AuthorizedKeys
      OK "Appended bundle to $AuthorizedKeys"
      Remove-Item $tmp -Force
    } else { WARN "Bundle missing after scp" }
  } catch { WARN "scp failed: $($_.Exception.Message)" }
}

INFO "Done. Test: ssh admin-trading hostname"
