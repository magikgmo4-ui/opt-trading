# Install TV Orchestrator Agent as OnLogon scheduled task (cursor-ai)
# Run once as Administrator, then the agent starts automatically on login.
# Usage: powershell -File install_agent.ps1

$ErrorActionPreference = 'Stop'

$TASK_NAME   = "TVOrchestratorAgent"
$AGENT_ROOT  = Split-Path $PSScriptRoot -Parent
$AGENT_SCRIPT = Join-Path $PSScriptRoot "tv_agent.ps1"
$LOG_DIR     = Join-Path $PSScriptRoot ""

Write-Host "Installing TVOrchestratorAgent scheduled task..." -ForegroundColor Cyan
Write-Host "  Script: $AGENT_SCRIPT"

$action  = New-ScheduledTaskAction `
    -Execute "powershell" `
    -Argument "-NoProfile -WindowStyle Hidden -File `"$AGENT_SCRIPT`""

$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $TASK_NAME `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -RunLevel Highest `
    -Force | Out-Null

Write-Host "PASS: Task '$TASK_NAME' registered (OnLogon, Highest)" -ForegroundColor Green
Write-Host ""
Write-Host "To start immediately (without re-login):"
Write-Host "  Start-ScheduledTask -TaskName '$TASK_NAME'"
Write-Host ""
Write-Host "To check status:"
Write-Host "  Get-ScheduledTask -TaskName '$TASK_NAME' | Get-ScheduledTaskInfo"
