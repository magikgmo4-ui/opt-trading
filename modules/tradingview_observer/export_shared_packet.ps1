# TradingView Observer -> Shared Packet Export (Option B)
# Dry-run safe: exports bridge packet to staging folder.
# No automatic transfer, no SSH, no admin-trading ingestion.
# Usage: .\export_shared_packet.ps1 [-OutputDir <path>] [-DryRun]
param(
    [string]$OutputDir = (Join-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) "_shared_packets\tradingview_observer"),
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$MOD = $PSScriptRoot
$BRIDGE_SCRIPT = Join-Path $MOD "export_bridge_packet.ps1"
$BRIDGE_PACKET = Join-Path $MOD "output\latest_bridge_packet.json"

if (-not (Test-Path $BRIDGE_PACKET)) {
    Write-Host "Bridge packet not found. Generating..." -ForegroundColor Yellow
    & $BRIDGE_SCRIPT
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FATAL: bridge packet generation failed" -ForegroundColor Red
        exit 1
    }
    if (-not (Test-Path $BRIDGE_PACKET)) {
        Write-Host "FATAL: bridge packet still missing after generation" -ForegroundColor Red
        exit 1
    }
}

$timestamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
$packetContent = Get-Content $BRIDGE_PACKET -Raw -Encoding UTF8
$packetObj = $packetContent | ConvertFrom-Json

$symbol = if ($packetObj.PSObject.Properties['symbol']) { $packetObj.symbol -replace '[<>:"/\\|?*]', '_' } else { "UNKNOWN" }
$timeframe = if ($packetObj.PSObject.Properties['timeframe']) { $packetObj.timeframe } else { "UNK" }

$stagedName = "${symbol}_${timeframe}min_${timestamp}_bridge_packet_v1.json"
$latestName = "latest_bridge_packet.json"

$symDir = Join-Path $OutputDir $symbol
$stagedPath = Join-Path $symDir $stagedName
$latestPath = Join-Path $symDir $latestName

if ($DryRun) {
    Write-Host "=== DRY-RUN Shared Packet Export ===" -ForegroundColor Cyan
    Write-Host "  Source   : $BRIDGE_PACKET" -ForegroundColor Gray
    Write-Host "  Staging  : $OutputDir" -ForegroundColor Gray
    Write-Host "  Symbol   : $symbol @ ${timeframe}min" -ForegroundColor Gray
    Write-Host "  Timestamp: $timestamp" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Would create:" -ForegroundColor Gray
    Write-Host "    $stagedPath" -ForegroundColor Cyan
    Write-Host "    $latestPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Alerts : $($packetObj.alerts_summary.total) total, $($packetObj.alerts_summary.active) active" -ForegroundColor Gray
    Write-Host "  Limits : webhook_visible=$($packetObj.limits.webhook_payload_visible), trading_mutation=$($packetObj.limits.trading_mutation_allowed)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  NO network. NO admin-trading. NO transfer." -ForegroundColor Yellow
    exit 0
}

Write-Host "=== Shared Packet Export ===" -ForegroundColor Cyan
Write-Host "  Staging : $OutputDir" -ForegroundColor Gray

New-Item -ItemType Directory -Force $symDir | Out-Null

# Copy as timestamped artifact
Copy-Item $BRIDGE_PACKET $stagedPath -Force
Write-Host "  Created : $stagedPath" -ForegroundColor Green

# Copy as latest (overwrite)
Copy-Item $BRIDGE_PACKET $latestPath -Force
Write-Host "  Latest  : $latestPath" -ForegroundColor Green

$sizeKB = [math]::Round((Get-Item $stagedPath).Length / 1KB, 1)
Write-Host ""
Write-Host "  Symbol  : $symbol @ ${timeframe}min" -ForegroundColor Cyan
Write-Host "  Size    : ${sizeKB} KB" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: transfer manually via WinSCP to:" -ForegroundColor Yellow
Write-Host "  /srv/sftp/shared_files/shared/tradingview_observer/" -ForegroundColor Gray
Write-Host ""
Write-Host "NO automatic transfer executed. NO admin-trading ingestion." -ForegroundColor Green
