# TradingView Observer -- OpenClaw Safe Runner
param([string]$Action = "sanity")

$WRAPPER = Join-Path $PSScriptRoot "..\tradingview_observer\cmd.ps1" -Resolve
$OUTPUT  = Join-Path $PSScriptRoot "..\tradingview_observer\output" -Resolve

if (-not (Test-Path $WRAPPER)) {
    Write-Host "FATAL: Wrapper not found" -ForegroundColor Red
    exit 1
}

if ($Action -eq "sanity") {
    Write-Host "=== OpenClaw TradingView Observer : Sanity ===" -ForegroundColor Cyan
    & $WRAPPER -Sanity
    exit $LASTEXITCODE
}

if ($Action -eq "snapshot") {
    Write-Host "=== OpenClaw TradingView Observer : Snapshot ===" -ForegroundColor Cyan
    & $WRAPPER -Sanity
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Sanity failed. Snapshot aborted." -ForegroundColor Yellow
        exit $LASTEXITCODE
    }
    Write-Host ""
    & $WRAPPER -Export
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Snapshot complete." -ForegroundColor Green
        Write-Host "Outputs:" -ForegroundColor Gray
        Get-ChildItem "$OUTPUT\latest_*.json" | ForEach-Object {
            $kb = [math]::Round($_.Length/1KB, 1)
            Write-Host "  $($_.Name) ($kb KB)" -ForegroundColor Gray
        }
        Write-Host ""
        Write-Host "Read $OUTPUT\latest_report.json for full analysis." -ForegroundColor Green
    }
    exit $LASTEXITCODE
}

Write-Host "Usage: .\run.ps1 [sanity|snapshot]" -ForegroundColor Yellow
exit 1
