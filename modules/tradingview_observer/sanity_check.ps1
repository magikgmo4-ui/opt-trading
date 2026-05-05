# TradingView Observer — Sanity Check
param(
    [int]$TimeoutSec = 10
)

$ErrorActionPreference = 'Stop'
$TV_MCP_CLI = "$env:USERPROFILE\.claude\tools\tradingview-mcp\src\cli\index.js"
$CDP_URL = "http://127.0.0.1:9222/json/version"
$PassCount = 0
$FailCount = 0

function Write-Check($Label, $Ok, $Detail) {
    if ($Ok) {
        Write-Host "[PASS] $Label" -ForegroundColor Green
        $script:PassCount++
    } else {
        Write-Host "[FAIL] $Label  --  $Detail" -ForegroundColor Red
        $script:FailCount++
    }
}

Write-Host "=== TradingView Observer Sanity Check ===" -ForegroundColor Cyan

# 1. Node.js
try { $v = & node --version 2>&1; Write-Check "Node.js" $true $v } catch { Write-Check "Node.js" $false $_.Exception.Message; exit 1 }

# 2. tradingview-mcp CLI
if (Test-Path $TV_MCP_CLI) { Write-Check "tradingview-mcp CLI" $true $TV_MCP_CLI } else { Write-Check "tradingview-mcp CLI" $false "Not found"; exit 1 }

# 3. CDP port 9222
try {
    $r = Invoke-WebRequest -Uri $CDP_URL -UseBasicParsing -TimeoutSec $TimeoutSec
    $json = $r.Content | ConvertFrom-Json
    Write-Check "CDP port 9222" $true $json.Browser
} catch {
    Write-Check "CDP port 9222" $false "TV not running or port closed"
}

# 4. tv status
if ($PassCount -ge 3) {
    try {
        $s = & node $TV_MCP_CLI status 2>&1 | Out-String | ConvertFrom-Json
        if ($s.success) { Write-Check "tv status" $true "$($s.chart_symbol) $($s.chart_resolution)" }
        else { Write-Check "tv status" $false "cdp_connected=$($s.cdp_connected)" }
    } catch { Write-Check "tv status" $false $_.Exception.Message }
}

# 5. tv state
if ($PassCount -ge 4) {
    try {
        $st = & node $TV_MCP_CLI state 2>&1 | Out-String | ConvertFrom-Json
        if ($st.success) { Write-Check "tv state" $true "$($st.symbol) studies=$($st.studies.Count)" }
        else { Write-Check "tv state" $false "fail" }
    } catch { Write-Check "tv state" $false $_.Exception.Message }
}

# 6. tv quote
if ($PassCount -ge 5) {
    try {
        $q = & node $TV_MCP_CLI quote 2>&1 | Out-String | ConvertFrom-Json
        if ($q.success) { Write-Check "tv quote" $true "$($q.symbol) close=$($q.close)" }
        else { Write-Check "tv quote" $false "fail" }
    } catch { Write-Check "tv quote" $false $_.Exception.Message }
}

# 7. tv alert list
if ($PassCount -ge 6) {
    try {
        $a = & node $TV_MCP_CLI alert list 2>&1 | Out-String | ConvertFrom-Json
        if ($a.success) { Write-Check "tv alert list" $true "count=$($a.alert_count)" }
        else { Write-Check "tv alert list" $false "fail" }
    } catch { Write-Check "tv alert list" $false $_.Exception.Message }
}

$color = if ($FailCount -eq 0) { "Green" } else { "Yellow" }
Write-Host "=== $PassCount PASS / $FailCount FAIL ===" -ForegroundColor $color
exit $FailCount
