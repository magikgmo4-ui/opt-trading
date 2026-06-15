# TradingView Observer Runner
# Read-only JSON exporter. Mutation requires -AllowMutation flag.
param(
    [switch]$AllowMutation,
    [string]$OutputDir = ""
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$TV_CLI = "$env:USERPROFILE\.claude\tools\tradingview-mcp\src\cli\index.js"
$CDP_URL = "http://127.0.0.1:9222/json/version"

if (-not $OutputDir) {
    $OutputDir = Join-Path $PSScriptRoot "..\output" -Resolve
}
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Force $OutputDir | Out-Null
}

if (-not (Test-Path $TV_CLI)) {
    Write-Host "FATAL: tradingview-mcp CLI not found at:" -ForegroundColor Red
    Write-Host "  $TV_CLI" -ForegroundColor Red
    Write-Host "Install: PR #76 MSIX merge required" -ForegroundColor Yellow
    exit 1
}

function Tv {
    $raw = & node $TV_CLI @args 2>&1 | Out-String
    try { $raw | ConvertFrom-Json }
    catch { Write-Host "  JSON parse failed for: tv $($args -join ' ')" -ForegroundColor Yellow; @{success=$false;error="json_parse_failed"} }
}

function Export-Json($Data, $Path) {
    $Data | Add-Member -NotePropertyName '_exported_at' -NotePropertyValue (Get-Date -Format 'o') -Force
    $json = $Data | ConvertTo-Json -Depth 10
    $json = $json -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($Path, $json, [System.Text.UTF8Encoding]::new($false))
    $size = [math]::Round((Get-Item $Path).Length / 1KB, 1)
    "  -> $($Path | Split-Path -Leaf) (${size} KB)"
}

$m = if ($AllowMutation) { "MUTATION" } else { "READ-ONLY" }
Write-Host "=== TradingView Observer Runner (${m}) ===" -ForegroundColor Cyan
Write-Host "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "Output: $OutputDir"
Write-Host ""

$exportCount = 0
$errorCount = 0

# 1. CDP check
Write-Host "[1/6] CDP check..."
try {
    $c = (Invoke-WebRequest $CDP_URL -UseBasicParsing -TimeoutSec 5).Content | ConvertFrom-Json
    Write-Host "  OK: $($c.Browser)" -ForegroundColor Green
} catch {
    Write-Host "  FAIL: port 9222 closed - TradingView Desktop not running" -ForegroundColor Red
    exit 1
}

# 2. tv status
Write-Host "[2/6] tv status..."
try {
    $s = Tv status
    if ($s.success) {
        Write-Host "  OK: $($s.chart_symbol) @ $($s.chart_resolution)min" -ForegroundColor Green
        Export-Json $s "$OutputDir\latest_status.json"
        $exportCount++
    } else {
        Write-Host "  FAIL: cdp_connected=$($s.cdp_connected)" -ForegroundColor Red
        $errorCount++; $s = @{success=$false;error="cdp not connected"}
    }
} catch {
    Write-Host "  FAIL: $_" -ForegroundColor Red
    $errorCount++; $s = @{success=$false;error="$_"}
}

# 3. tv quote
Write-Host "[3/6] tv quote..."
try {
    $q = Tv quote
    if ($q.success) {
        Write-Host "  OK: $($q.symbol) close=$($q.close)" -ForegroundColor Green
        Export-Json $q "$OutputDir\latest_quote.json"
        $exportCount++
    } else {
        Write-Host "  FAIL" -ForegroundColor Red
        $errorCount++; $q = @{success=$false;error="quote failed"}
    }
} catch {
    Write-Host "  FAIL: $_" -ForegroundColor Red
    $errorCount++; $q = @{success=$false;error="$_"}
}

# 4. tv state
Write-Host "[4/6] tv state..."
try {
    $st = Tv state
    if ($st.success) {
        Write-Host "  OK: $($st.symbol) studies=$($st.studies.Count)" -ForegroundColor Green
        Export-Json $st "$OutputDir\latest_state.json"
        $exportCount++
    } else {
        Write-Host "  FAIL" -ForegroundColor Red
        $errorCount++; $st = @{success=$false;error="state failed"}
    }
} catch {
    Write-Host "  FAIL: $_" -ForegroundColor Red
    $errorCount++; $st = @{success=$false;error="$_"}
}

# 5. tv alert list
Write-Host "[5/6] tv alert list..."
try {
    $a = Tv alert list
    if ($a.success) {
        Write-Host "  OK: $($a.alert_count) alerts" -ForegroundColor Green
        Export-Json $a "$OutputDir\latest_alert_inventory.json"
        $exportCount++
    } else {
        Write-Host "  FAIL" -ForegroundColor Red
        $errorCount++; $a = @{success=$false;error="alert list failed"}
    }
} catch {
    Write-Host "  FAIL: $_" -ForegroundColor Red
    $errorCount++; $a = @{success=$false;error="$_"}
}

# 6. tv values
Write-Host "[6/6] tv values..."
try {
    $v = Tv values
    if ($v.success) {
        Write-Host "  OK: $($v.study_count) indicators visible" -ForegroundColor Green
        Export-Json $v "$OutputDir\latest_values.json"
        $exportCount++
    } else {
        Write-Host "  FAIL (indicators may not be loaded on current TV layout)" -ForegroundColor Yellow
        $errorCount++; $v = @{success=$false;error="values failed"}
    }
} catch {
    Write-Host "  FAIL: $_" -ForegroundColor Red
    $errorCount++; $v = @{success=$false;error="$_"}
}

# Combined report
$report = [ordered]@{
    exported_at     = (Get-Date -Format 'o')
    mode            = $m
    status          = $s
    state           = $st
    quote           = $q
    alert_inventory = $a
    values          = $v
}

$reportJson = $report | ConvertTo-Json -Depth 10
$reportJson = $reportJson -replace "`r`n", "`n"
[System.IO.File]::WriteAllText("$OutputDir\latest_report.json", $reportJson, [System.Text.UTF8Encoding]::new($false))

Write-Host ""
Write-Host "=== Export Results ===" -ForegroundColor Cyan
Write-Host "  Exports: $exportCount/6" -ForegroundColor $(if ($exportCount -ge 5) { "Green" } else { "Yellow" })
Write-Host "  Errors : $errorCount/6" -ForegroundColor $(if ($errorCount -eq 0) { "Green" } else { "Yellow" })
Write-Host ""
Get-ChildItem "$OutputDir\latest_*.json" -Exclude "latest_bridge_packet.json" | ForEach-Object {
    $kb = [math]::Round($_.Length / 1KB, 1)
    Write-Host "  $($_.Name) (${kb} KB)" -ForegroundColor Gray
}

Write-Host ""
$p = if ($exportCount -ge 4) { "Green" } else { "Yellow" }
Write-Host "Report: $OutputDir\latest_report.json" -ForegroundColor $p

exit $(if ($errorCount -gt 0 -and $exportCount -lt 3) { 1 } else { 0 })
