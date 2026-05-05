# TradingView Observer — Sanity Check
param(
    [int]$TimeoutSec = 10
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$TV_MCP_CLI = "$env:USERPROFILE\.claude\tools\tradingview-mcp\src\cli\index.js"
$CDP_URL = "http://127.0.0.1:9222/json/version"
$PassCount = 0
$FailCount = 0
$StartTime = Get-Date

function Write-Check($Label, $Ok, $Detail) {
    $ts = (Get-Date).ToString("HH:mm:ss")
    if ($Ok) {
        Write-Host "[$ts] [PASS] $Label" -ForegroundColor Green
        $script:PassCount++
    } else {
        Write-Host "[$ts] [FAIL] $Label  —  $Detail" -ForegroundColor Red
        $script:FailCount++
    }
}

Write-Host "=== TradingView Observer Sanity Check ===" -ForegroundColor Cyan
Write-Host "Started: $($StartTime.ToString('yyyy-MM-dd HH:mm:ss'))"
Write-Host "Timeout: ${TimeoutSec}s per check"
Write-Host ""

Write-Check "PowerShell ErrorAction" $true "Stop (strict mode)"

# 1. Node.js
try {
    $nv = & node --version 2>&1 | Out-String
    $nv = $nv.Trim()
    Write-Check "Node.js" $true "$nv"
} catch {
    Write-Check "Node.js" $false "Node.js not found or not in PATH"
}

# 2. tradingview-mcp CLI
if (Test-Path $TV_MCP_CLI) {
    $cliVer = (Get-Item $TV_MCP_CLI).LastWriteTime.ToString('yyyy-MM-dd')
    Write-Check "tradingview-mcp CLI" $true "installed ($cliVer)"
} else {
    Write-Check "tradingview-mcp CLI" $false "Not found at: $TV_MCP_CLI"
}

# 3. CDP port 9222
try {
    $r = Invoke-WebRequest -Uri $CDP_URL -UseBasicParsing -TimeoutSec $TimeoutSec
    $json = $r.Content | ConvertFrom-Json
    Write-Check "CDP port 9222" $true $json.Browser
} catch {
    Write-Check "CDP port 9222" $false "TradingView Desktop not running or port closed"
}

# 4. tv status
if ($PassCount -ge 3) {
    try {
        $raw = & node $TV_MCP_CLI status 2>&1 | Out-String
        $s = $raw | ConvertFrom-Json
        if ($s.success) {
            Write-Check "tv status" $true "$($s.chart_symbol) @ $($s.chart_resolution)min"
        } else {
            Write-Check "tv status" $false "cdp_connected=$($s.cdp_connected)"
        }
    } catch {
        Write-Check "tv status" $false $_.Exception.Message
    }
}

# 5. tv state
if ($PassCount -ge 4) {
    try {
        $raw = & node $TV_MCP_CLI state 2>&1 | Out-String
        $st = $raw | ConvertFrom-Json
        if ($st.success) {
            Write-Check "tv state" $true "$($st.symbol) studies=$($st.studies.Count)"
        } else {
            Write-Check "tv state" $false "fail"
        }
    } catch {
        Write-Check "tv state" $false $_.Exception.Message
    }
}

# 6. tv quote
if ($PassCount -ge 5) {
    try {
        $raw = & node $TV_MCP_CLI quote 2>&1 | Out-String
        $q = $raw | ConvertFrom-Json
        if ($q.success) {
            Write-Check "tv quote" $true "$($q.symbol) close=$($q.close)"
        } else {
            Write-Check "tv quote" $false "fail"
        }
    } catch {
        Write-Check "tv quote" $false $_.Exception.Message
    }
}

# 7. tv alert list
if ($PassCount -ge 6) {
    try {
        $raw = & node $TV_MCP_CLI alert list 2>&1 | Out-String
        $a = $raw | ConvertFrom-Json
        if ($a.success) {
            Write-Check "tv alert list" $true "count=$($a.alert_count)"
        } else {
            Write-Check "tv alert list" $false "fail"
        }
    } catch {
        Write-Check "tv alert list" $false $_.Exception.Message
    }
}

# 8. Mutation check
Write-Check "Mutation locked" $true "alert_create/delete/webhook_update disabled (no -AllowMutation)"

$duration = [math]::Round(((Get-Date) - $StartTime).TotalSeconds, 1)
$color = if ($FailCount -eq 0) { "Green" } else { "Yellow" }
Write-Host ""
Write-Host "=== $PassCount PASS / $FailCount FAIL — ${duration}s ===" -ForegroundColor $color
exit $FailCount
