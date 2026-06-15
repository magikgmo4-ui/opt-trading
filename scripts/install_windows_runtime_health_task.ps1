param(
    [string]$TaskName = "OptTradingRuntimeHealthCursorAi",
    [string]$Machine = "cursor-ai",
    [int]$IntervalMinutes = 5
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

$Python = $null
try {
    $Python = (& py -3 -c "import sys; print(sys.executable)" 2>$null | Select-Object -First 1).Trim()
} catch {
    $Python = $null
}
if (-not $Python -or -not (Test-Path $Python)) {
    $Python = (Get-Command python -ErrorAction Stop).Source
}

$healthArgs = @(
    "-m", "modules.runtime_health.healthcheck",
    "--config", "modules/runtime_health/config/runtime_health.yml",
    "--map", "config/machine_runtime_map.yml",
    "--machine", $Machine,
    "--no-telegram"
) -join " "

$action = New-ScheduledTaskAction -Execute $Python -Argument $healthArgs -WorkingDirectory $RepoRoot

$repeatTrigger = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes) `
    -RepetitionDuration (New-TimeSpan -Days 3650)

$logonTrigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 2)

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger @($repeatTrigger, $logonTrigger) `
    -Settings $settings `
    -Description "opt-trading runtime healthcheck for cursor-ai every $IntervalMinutes minutes" `
    -User $env:USERNAME `
    -Force | Out-Null

Start-ScheduledTask -TaskName $TaskName

Get-ScheduledTask -TaskName $TaskName |
    Select-Object TaskName, State, TaskPath
