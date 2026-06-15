# Install TV Orchestrator Agent as OnLogon scheduled task (cursor-ai)
# Run once as Administrator, then the agent starts automatically on login.
# Usage: powershell -File install_agent.ps1

$ErrorActionPreference = 'Stop'

$TASK_NAME   = "TVOrchestratorAgent"
$WATCHDOG_TASK_NAME = "TVOrchestratorAgentWatchdog"
$AGENT_ROOT  = Split-Path $PSScriptRoot -Parent
$AGENT_SCRIPT = Join-Path $PSScriptRoot "tv_agent.ps1"
$LOG_DIR     = Join-Path $PSScriptRoot ""

Write-Host "Installing TVOrchestratorAgent scheduled task..." -ForegroundColor Cyan
Write-Host "  Script: $AGENT_SCRIPT"

$action  = New-ScheduledTaskAction `
    -Execute "powershell" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$AGENT_SCRIPT`"" `
    -WorkingDirectory $AGENT_ROOT

$logonTrigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$watchdogTrigger = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes 5) `
    -RepetitionDuration (New-TimeSpan -Days 3650)

$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0) `
    -RestartCount 5 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -MultipleInstances IgnoreNew `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

try {
    Register-ScheduledTask `
        -TaskName $TASK_NAME `
        -Action $action `
        -Trigger @($logonTrigger, $watchdogTrigger) `
        -Settings $settings `
        -RunLevel Highest `
        -Force | Out-Null

    Write-Host "PASS: Task '$TASK_NAME' registered (OnLogon + 5min watchdog, Highest)" -ForegroundColor Green
} catch {
    Write-Warning "Could not update '$TASK_NAME' with RunLevel Highest: $($_.Exception.Message)"
}

Register-ScheduledTask `
    -TaskName $WATCHDOG_TASK_NAME `
    -Action $action `
    -Trigger $watchdogTrigger `
    -Settings $settings `
    -Force | Out-Null

Write-Host "PASS: Task '$WATCHDOG_TASK_NAME' registered (5min watchdog, user-level)" -ForegroundColor Green
Write-Host ""
Write-Host "To start immediately (without re-login):"
Write-Host "  Start-ScheduledTask -TaskName '$TASK_NAME'"
Write-Host ""
Write-Host "To check status:"
Write-Host "  Get-ScheduledTask -TaskName '$TASK_NAME' | Get-ScheduledTaskInfo"
