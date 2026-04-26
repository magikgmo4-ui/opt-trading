param(
  [string]$User = $env:USERNAME,
  [string]$PublicKey = ""
)

$sshDir = Join-Path $env:USERPROFILE ".ssh"
$ak = Join-Path $sshDir "authorized_keys"

New-Item -ItemType Directory -Force -Path $sshDir | Out-Null
if (!(Test-Path $ak)) { New-Item -ItemType File -Force -Path $ak | Out-Null }

# Remove inheritance and set strict ACL: SYSTEM + user full control
icacls $sshDir /inheritance:r | Out-Null
icacls $sshDir /grant "SYSTEM:(OI)(CI)F" | Out-Null
icacls $sshDir /grant "$User:(OI)(CI)F" | Out-Null

icacls $ak /inheritance:r | Out-Null
icacls $ak /grant "SYSTEM:F" | Out-Null
icacls $ak /grant "$User:F" | Out-Null

if ($PublicKey -ne "") {
  $content = Get-Content $ak -ErrorAction SilentlyContinue
  if ($content -notcontains $PublicKey) {
    Add-Content -Path $ak -Value $PublicKey
    Write-Host "OK: public key appended to $ak"
  } else {
    Write-Host "OK: public key already present"
  }
}

Write-Host "OK: ACL fixed for $sshDir and $ak"
Write-Host "TIP: restart OpenSSH Server if needed: Restart-Service sshd"
