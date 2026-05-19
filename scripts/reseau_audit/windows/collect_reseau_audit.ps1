$ErrorActionPreference = "Stop"
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$hostn = $env:COMPUTERNAME
$outRoot = Join-Path $env:TEMP "reseau_audit_$hostn`_$ts"
New-Item -ItemType Directory -Force -Path $outRoot | Out-Null
function Run-ToFile($name, $cmd) {
  $p = Join-Path $outRoot $name
  "### CMD: $cmd" | Out-File -FilePath $p -Encoding utf8
  "### TIME: $(Get-Date -Format o)" | Out-File -FilePath $p -Append -Encoding utf8
  "" | Out-File -FilePath $p -Append -Encoding utf8
  try { Invoke-Expression $cmd | Out-File -FilePath $p -Append -Encoding utf8 }
  catch { $_ | Out-File -FilePath $p -Append -Encoding utf8 }
}
Run-ToFile "00_system.txt" "systeminfo | Select-Object -First 80"
Run-ToFile "01_ipconfig.txt" "ipconfig /all"
Run-ToFile "02_routes.txt" "route print"
Run-ToFile "03_dns.txt" "Get-DnsClientServerAddress | Format-List"
Run-ToFile "04_firewall_rules.txt" "Get-NetFirewallRule | Where-Object {$_.DisplayName -like '*reseau*' -or $_.DisplayName -like '*SSH*' -or $_.DisplayName -like '*WireGuard*'} | Select-Object DisplayName,Enabled,Direction,Action,Profile | Format-Table -AutoSize"
Run-ToFile "05_openssh_service.txt" "Get-Service sshd -ErrorAction SilentlyContinue | Format-List *"
Run-ToFile "06_openssh_config.txt" "if (Test-Path 'C:\ProgramData\ssh\sshd_config') { Get-Content 'C:\ProgramData\ssh\sshd_config' } else { 'no sshd_config found' }"
Run-ToFile "07_authorized_keys_acl.txt" "icacls $env:USERPROFILE\.ssh\authorized_keys 2>&1"
Run-ToFile "08_wireguard.txt" "Get-Process -Name wireguard -ErrorAction SilentlyContinue | Select-Object -First 5 | Format-Table -AutoSize; Get-NetUDPEndpoint | Where-Object {$_.LocalPort -in 51820,51821} | Select-Object -First 80 | Format-Table -AutoSize"
$summary = Join-Path $outRoot "summary.txt"
@("reseau_audit v1.3 (Windows)","host=$hostn","time=$(Get-Date -Format o)") | Out-File -FilePath $summary -Encoding utf8
$zip = Join-Path $env:USERPROFILE "Downloads\reseau_audit_$hostn`_$ts.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path (Join-Path $outRoot "*") -DestinationPath $zip
Write-Host "OK: zip: $zip"
