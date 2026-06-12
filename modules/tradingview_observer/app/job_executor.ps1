# TradingView Observer — Job Executor
# Called by tv_runner.py via SSH with a SCP'd PS1 payload.
# This file is NOT called directly — it is invoked by tv_runner.py dynamically.
#
# Each job type generates a self-contained PS1 script that sources this helper,
# then executes its specific logic. This file documents the pattern.
#
# Mutation guard: any script arriving with mutation logic must have been
# approved via --gate-approved on the admin-trading side before SSH dispatch.

$ErrorActionPreference = 'Stop'

$TV_CLI = "$env:USERPROFILE\.claude\tools\tradingview-mcp\src\cli\index.js"

if (-not (Test-Path $TV_CLI)) {
    @{success=$false; error="tradingview-mcp CLI not found at $TV_CLI"} | ConvertTo-Json
    exit 1
}

function Tv {
    $raw = & node $TV_CLI @args 2>&1 | Out-String
    try   { $raw | ConvertFrom-Json }
    catch { @{success=$false; error="json_parse_failed"; raw=$raw} }
}

# CDP check
try {
    $cdp = (Invoke-WebRequest "http://127.0.0.1:9222/json/version" -UseBasicParsing -TimeoutSec 5).Content | ConvertFrom-Json
    Write-Host "CDP OK: $($cdp.Browser)" -ForegroundColor Green
} catch {
    @{success=$false; error="CDP connection failed — TradingView Desktop not running or CDP not on port 9222"} | ConvertTo-Json
    exit 1
}
