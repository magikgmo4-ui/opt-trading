\
param(
  [string]$OutDir = "snapshot"
)

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$ts = (Get-Date).ToString("yyyy-MM-ddTHH-mm-ss")
$out = Join-Path $OutDir ("snapshot_" + $ts + ".txt")

"=== SANITIZED MACHINE SNAPSHOT (WINDOWS) ===" | Out-File $out -Encoding utf8
(Get-Date).ToString("o") | Out-File $out -Append

"`n[host]" | Out-File $out -Append
hostname | Out-File $out -Append

"`n[os]" | Out-File $out -Append
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsHardwareAbstractionLayer | Format-List | Out-File $out -Append

"`n[cpu]" | Out-File $out -Append
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors | Format-List | Out-File $out -Append

"`n[memory]" | Out-File $out -Append
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory | Format-List | Out-File $out -Append

"`n[disks]" | Out-File $out -Append
Get-Volume | Select-Object DriveLetter, FileSystemLabel, FileSystem, SizeRemaining, Size | Format-Table -AutoSize | Out-File $out -Append

"`n[network]" | Out-File $out -Append
Get-NetIPConfiguration | Format-List | Out-File $out -Append

"`n[ports listening (top)]" | Out-File $out -Append
netstat -ano | Select-String "LISTENING" | Select-Object -First 120 | Out-File $out -Append

"`n[cursor]" | Out-File $out -Append
"Optional Cursor logs path: C:\Users\ghost\.cursor\logs" | Out-File $out -Append

"`n[redaction note]" | Out-File $out -Append
"Do NOT paste tokens, keys, repo URLs, public IPs, emails. Scan this file before sharing." | Out-File $out -Append

Write-Host ("Wrote: " + $out)
