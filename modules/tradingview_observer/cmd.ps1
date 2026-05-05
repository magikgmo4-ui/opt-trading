# TradingView Observer — Wrapper CLI
# Usage: .\cmd.ps1 [-Sanity] [-Export] [-AllowMutation]
param([switch]$Sanity, [switch]$Export, [switch]$AllowMutation)

$MOD = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($Sanity) {
    & "$MOD\sanity_check.ps1"
    exit $LASTEXITCODE
}

if ($AllowMutation) {
    Write-Host "WARNING: Mutation mode enabled" -ForegroundColor Magenta
}

if ($Export) {
    & "$MOD\app\observer_runner.ps1" -AllowMutation:$AllowMutation
    exit $LASTEXITCODE
}

# Default: sanity + export
Write-Host "TradingView Observer Wrapper" -ForegroundColor Cyan
Write-Host ""

& "$MOD\sanity_check.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Sanity check failed. Export skipped." -ForegroundColor Yellow
    exit $LASTEXITCODE
}

Write-Host ""
& "$MOD\app\observer_runner.ps1" -AllowMutation:$AllowMutation
