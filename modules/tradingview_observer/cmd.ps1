# TradingView Observer — Wrapper CLI
# Usage: .\cmd.ps1 [-Sanity] [-Export] [-Snapshot] [-Bridge] [-AllowMutation]
param(
    [switch]$Sanity,
    [switch]$Export,
    [switch]$Snapshot,
    [switch]$Bridge,
    [switch]$AllowMutation
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$MOD = $PSScriptRoot

$ALLOWED_MODES = @('sanity', 'snapshot', 'bridge', 'status', 'state', 'quote', 'values', 'alerts')
$FORBIDDEN_MODES = @('alert_create', 'alert_delete', 'webhook_update', 'trade', 'mutation', 'admin_push')

if ($AllowMutation) {
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host "  WARNING: MUTATION MODE ENABLED" -ForegroundColor Magenta
    Write-Host "  This bypasses read-only protections." -ForegroundColor Magenta
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host ""
}

if ($Bridge) {
    Write-Host "TradingView Observer — Bridge Packet Export" -ForegroundColor Cyan
    Write-Host ""
    & "$MOD\export_bridge_packet.ps1"
    exit $LASTEXITCODE
}

if ($Sanity) {
    & "$MOD\sanity_check.ps1"
    exit $LASTEXITCODE
}

if ($Snapshot -or $Export) {
    Write-Host "TradingView Observer Wrapper" -ForegroundColor Cyan
    Write-Host ""

    & "$MOD\sanity_check.ps1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Sanity check failed. Snapshot skipped." -ForegroundColor Yellow
        exit $LASTEXITCODE
    }

    Write-Host ""
    & "$MOD\app\observer_runner.ps1" -AllowMutation:$AllowMutation
    exit $LASTEXITCODE
}

Write-Host "TradingView Observer Wrapper" -ForegroundColor Cyan
Write-Host ""

Write-Host "Usage:" -ForegroundColor Gray
Write-Host "  .\cmd.ps1                 : sanity + export (full default)" -ForegroundColor Gray
Write-Host "  .\cmd.ps1 -Sanity         : sanity check only" -ForegroundColor Gray
Write-Host "  .\cmd.ps1 -Snapshot       : sanity + full JSON export" -ForegroundColor Gray
Write-Host "  .\cmd.ps1 -Bridge         : bridge packet export (dry-run)" -ForegroundColor Gray
Write-Host ""
Write-Host "Modes: $($ALLOWED_MODES -join ', ')" -ForegroundColor Gray
if (-not $AllowMutation) {
    Write-Host ""
    Write-Host "Mutation disabled. Use -AllowMutation to enable:" -ForegroundColor Yellow
    Write-Host "  alert_create, alert_delete, webhook_update" -ForegroundColor Yellow
}

exit 0
