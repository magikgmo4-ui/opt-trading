param(
    [string]$Machine = "cursor-ai"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$LogDir = Join-Path $RepoRoot "logs"
$LogPath = Join-Path $LogDir "runtime_health_windows_task.log"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
Set-Location $RepoRoot

$python = $null
try {
    $python = (& py -3 -c "import sys; print(sys.executable)" 2>$null | Select-Object -First 1).Trim()
} catch {
    $python = $null
}
if (-not $python -or -not (Test-Path $python)) {
    $python = (Get-Command python -ErrorAction Stop).Source
}

$argsList = @(
    "-m", "modules.runtime_health.healthcheck",
    "--config", "modules/runtime_health/config/runtime_health.yml",
    "--map", "config/machine_runtime_map.yml",
    "--machine", $Machine,
    "--no-telegram"
)

$stamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ssK")
"==== $stamp machine=$Machine ====" | Out-File -FilePath $LogPath -Append -Encoding utf8
"python=$python" | Out-File -FilePath $LogPath -Append -Encoding utf8

$stdoutPath = Join-Path $LogDir "runtime_health_windows_task.stdout.tmp"
$stderrPath = Join-Path $LogDir "runtime_health_windows_task.stderr.tmp"
Remove-Item $stdoutPath, $stderrPath -Force -ErrorAction SilentlyContinue

$proc = Start-Process `
    -FilePath $python `
    -ArgumentList $argsList `
    -WorkingDirectory $RepoRoot `
    -Wait `
    -PassThru `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath `
    -WindowStyle Hidden

$exitCode = $proc.ExitCode

$stdout = if (Test-Path $stdoutPath) { Get-Content -Path $stdoutPath -Raw -ErrorAction SilentlyContinue } else { "" }
$stderr = if (Test-Path $stderrPath) { Get-Content -Path $stderrPath -Raw -ErrorAction SilentlyContinue } else { "" }

if ($stdout) {
    $stdout | Write-Output
    $stdout | Out-File -FilePath $LogPath -Append -Encoding utf8
}
if ($stderr) {
    "STDERR:" | Out-File -FilePath $LogPath -Append -Encoding utf8
    $stderr | Out-File -FilePath $LogPath -Append -Encoding utf8
}
"exit=$exitCode" | Out-File -FilePath $LogPath -Append -Encoding utf8

exit $exitCode
