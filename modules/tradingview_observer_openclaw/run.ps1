# TradingView Observer -- OpenClaw Safe Runner
# Orchestrateur read-only. Ne jamais acceder directement a CDP ou tradingview-mcp.
# Usage: .\run.ps1 [sanity|snapshot|bridge]
param(
    [ValidateSet("sanity", "snapshot", "bridge")]
    [string]$Action = "sanity"
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$MOD = $PSScriptRoot
$WRAPPER = Join-Path $MOD "..\tradingview_observer\cmd.ps1" -Resolve
$OUTPUT  = Join-Path $MOD "..\tradingview_observer\output" -Resolve

if (-not (Test-Path $WRAPPER)) {
    Write-Host "FATAL: Wrapper not found at $WRAPPER" -ForegroundColor Red
    Write-Host "  Ensure modules/tradingview_observer/cmd.ps1 exists" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path $OUTPUT)) {
    New-Item -ItemType Directory -Force $OUTPUT | Out-Null
}

switch ($Action) {
    "sanity" {
        Write-Host "=== OpenClaw TradingView Observer : Sanity ===" -ForegroundColor Cyan
        $start = Get-Date
        & $WRAPPER -Sanity
        $ec = $LASTEXITCODE
        $dur = [math]::Round(((Get-Date) - $start).TotalSeconds, 1)
        Write-Host ""
        Write-Host "Sanity complete. Exit code: $ec (${dur}s)" -ForegroundColor $(if ($ec -eq 0) { "Green" } else { "Yellow" })
        exit $ec
    }

    "snapshot" {
        Write-Host "=== OpenClaw TradingView Observer : Snapshot ===" -ForegroundColor Cyan
        $start = Get-Date

        & $WRAPPER -Sanity
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Sanity failed. Snapshot aborted." -ForegroundColor Yellow
            exit $LASTEXITCODE
        }
        Write-Host ""
        & $WRAPPER -Snapshot
        $ec = $LASTEXITCODE

        if ($ec -eq 0) {
            Write-Host ""
            Write-Host "Snapshot complete." -ForegroundColor Green
            Write-Host "Outputs:" -ForegroundColor Gray
            Get-ChildItem "$OUTPUT\latest_*.json" -Exclude "latest_bridge_packet.json" | ForEach-Object {
                $kb = [math]::Round($_.Length / 1KB, 1)
                Write-Host "  $($_.Name) ($kb KB)" -ForegroundColor Gray
            }
            Write-Host ""
            Write-Host "Read $OUTPUT\latest_report.json for full analysis." -ForegroundColor Green
        }

        $dur = [math]::Round(((Get-Date) - $start).TotalSeconds, 1)
        Write-Host "Snapshot complete. Exit code: $ec (${dur}s)" -ForegroundColor $(if ($ec -eq 0) { "Green" } else { "Yellow" })
        exit $ec
    }

    "bridge" {
        Write-Host "=== OpenClaw TradingView Observer : Bridge Packet ===" -ForegroundColor Cyan
        $start = Get-Date

        & $WRAPPER -Bridge
        $ec = $LASTEXITCODE

        $dur = [math]::Round(((Get-Date) - $start).TotalSeconds, 1)

        if ($ec -eq 0) {
            $bp = Join-Path $OUTPUT "latest_bridge_packet.json"
            if (Test-Path $bp) {
                Write-Host ""
                Write-Host "Bridge packet ready:" -ForegroundColor Green
                Write-Host "  $bp" -ForegroundColor Gray
                Write-Host "  Size: $([math]::Round((Get-Item $bp).Length / 1KB, 1)) KB" -ForegroundColor Gray
            }
        }

        Write-Host "Bridge export complete. Exit code: $ec (${dur}s)" -ForegroundColor $(if ($ec -eq 0) { "Green" } else { "Yellow" })
        exit $ec
    }
}

Write-Host "Usage: .\run.ps1 [sanity|snapshot|bridge]" -ForegroundColor Yellow
Write-Host ""
Write-Host "  sanity   : infrastructure + TV health check (7 checks)" -ForegroundColor Gray
Write-Host "  snapshot : sanity + full JSON export (6 files)" -ForegroundColor Gray
Write-Host "  bridge   : bridge packet V1 export (dry-run, no transfer)" -ForegroundColor Gray
exit 1
